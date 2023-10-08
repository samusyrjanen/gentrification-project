 # 
# Inhabitants' median disposable monetary income by postal code area, 2010-2021:
# 
# https://pxdata.stat.fi:443/PxWeb/sq/39625562-d250-492a-a190-37bcc355e2a3
# 
# Prices per square meter of old dwellings in housing companies and numbers of transactions by postal code area, yearly, 2009-2022:
# 
# https://pxdata.stat.fi:443/PxWeb/sq/41826b15-82a9-4c83-8be6-bd77f98b31ac
#
import numpy as np
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

# Read in what we've got.
incomes = pd.read_csv('data/003_12f1_2021_20230929-100110.csv',
                      encoding = 'latin1',
                      na_values = [ '0' ],
                      skiprows = [0, 1])
prices = pd.read_csv('data/001_13mu_2022_20230929-105546.csv',
                     encoding = 'latin1',
                     na_values = [ '.', '..', '...' ],
                     skiprows = [0, 1])

# Drop unwanted columns for ease of use later on.
incomes.drop('Information', axis = 1, inplace = True)
prices.drop([ 'Building type', 'Information' ], axis = 1, inplace = True)

# Postal codes are unique, and they're also used as identifiers in GeoJSON
# containing borders of postal code areas; so, we might separate them from
# more traditional names.
prices.insert(
  loc = 1,
  column = 'Name',
  value = prices['Postal code'].map(lambda _: ' '.join(filter(lambda x: len(x) > 0,
                                                              _.split(' ')[1:])))
)
prices['Postal code'] = prices['Postal code'].map(lambda _: _.split(' ')[0])

incomes.insert(
  loc = 0,
  column = 'Name',
  value = incomes['Postal code area'].map(lambda _: ' '.join(filter(lambda x: len(x) > 0,
                                                                    _.split(' ')[1:])))
)
incomes.insert(loc = 0,
               column = 'Postal code',
               value = incomes['Postal code area'].map(lambda _: _.split(' ')[0]))
incomes.drop('Postal code area', axis = 1, inplace = True)

# 
# In ARIMA modelling below values P=3, Q=1, and D=4 are used. However, the values used
# originate from (an embarrassingly large set of) trial and error; so, this set of values
# might not be the best possible values. But, they're a set of values producing no
# negative predictions, which probably counts for this set's merit.
# 
# Documentation:
# 
#   https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html
#   https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.fit.html
# 
# Some background information for those who might be willing to wade through some:
# 
#   https://stats.stackexchange.com/questions/44992
#   https://blog.devgenius.io/finding-optimal-p-d-and-q-values-for-your-arima-model-94669a909a35
#   https://analyticsindiamag.com/quick-way-to-find-p-d-and-q-values-for-arima/
#

#
# Now, because not all time series are complete, and because P, Q, and D values
# are same for each time series, quite a hefty load of warnings would result.
# Since there's nothing we can do about those warnings as there's no way to
# tailor P, Q, and D values for each "row" of data individually, we might just
# as well prevent those warnings from cluttering our screens or log files.
#
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.simplefilter(action = 'ignore', category = ConvergenceWarning)
warnings.simplefilter(action = 'ignore', category = UserWarning)

# Compute predictions from time series in data.
income_predictions = []
income_deltas = []
income_percent_deltas = []

for r in range(0, incomes.shape[0]):
  history = incomes.drop(['Name', 'Postal code'], axis = 1).rename({ 3: 'Income' }).iloc[[r]].T
  history.index = pd.date_range(freq = 'AS-JAN',
                                periods = len(history.index),
                                start = history.index[0])
  model = ARIMA(history, enforce_stationarity = False, order = (3, 1, 4))
  fitted_model = model.fit()
  prediction = fitted_model.forecast().values[0]

  income_predictions.append(prediction)
  delta = prediction - incomes.iloc[r, incomes.shape[1] - 1]
  income_deltas.append(delta)
  income_percent_deltas.append((delta / prediction) * 100)

incomes.insert(column = str(int(incomes.columns[-1]) + 1),
               loc = incomes.shape[1],
               value = income_predictions)
incomes.insert(column = 'Delta',
               loc = incomes.shape[1],
               value = income_deltas)
incomes.insert(column = 'Delta Percent',
               loc = incomes.shape[1],
               value = income_percent_deltas)

price_predictions = []
price_deltas = []
price_percent_deltas = []

for r in range(0, prices.shape[0]):
  history = prices.drop(['Name', 'Postal code'], axis = 1).rename({ 3: 'Price' }).iloc[[r]].T
  history.index = pd.date_range(freq = 'AS-JAN',
                                periods = len(history.index),
                                start = history.index[0])
  model = ARIMA(history, enforce_stationarity = False, order = (3, 1, 4))
  fitted_model = model.fit()
  prediction = fitted_model.forecast().values[0]

  price_predictions.append(prediction)
  delta = prediction - prices.iloc[r, prices.shape[1] - 1]
  price_deltas.append(delta)
  price_percent_deltas.append((delta / prediction) * 100)

prices.insert(column = str(int(prices.columns[-1]) + 1),
              loc = prices.shape[1],
              value = price_predictions)
prices.insert(column = 'Delta',
              loc = prices.shape[1],
              value = price_deltas)
prices.insert(column = 'Delta Percent',
              loc = prices.shape[1],
              value = price_percent_deltas)

# Now that we've past time series analysis, warnings might be of some use again.
warnings.resetwarnings()

# Better ensure we're on the sane side of things with our P, Q, and D values.
assert incomes.loc[incomes['2022'] < 0].empty, "Oh dear, incomes can't be negative."
assert prices.loc[prices['2023'] < 0].empty, "Oh dear, prices can't be negative either."

# Compute results as one of the TAs suggested (take the mean of percentage changes).
results = pd.merge(prices[['Postal code', 'Delta Percent']],
                   incomes[['Postal code', 'Delta Percent']],
                   on = 'Postal code')
results['Percent Change'] = results.apply(lambda _: (_['Delta Percent_x'] + _['Delta Percent_y']) / 2, axis = 1)

# Turn the mean of percentage changes into a "gentrification score" with the trusty old logistic
# sigmoid function (w/ a vertical stretch and a vertical shift to get on the desired interval).
stretch = results['Percent Change'].map(lambda _: abs(_)).max()
results['Score'] = results['Percent Change'].map(lambda _: ((1 / (1 + np.exp(-(_/stretch)))) * 2) - 1)
results.index = results['Postal code']

from os import path

json_file = path.join('data', 'gentrification.json')
results[['Percent Change', 'Score']].to_json(json_file, indent = 2, orient = 'index')
print(f'Results written into "{json_file}".')

# end of file (this is here to make sure the last code line definitely ends with a new line).