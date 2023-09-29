# %%
import pandas as pd
import matplotlib.pyplot as plt

from random import randint
#from matplotlib import pyplot

# Data sources
#
#   - Inhabitants' median disposable monetary income by postal code area, 2010-2021
#     https://pxdata.stat.fi:443/PxWeb/sq/39625562-d250-492a-a190-37bcc355e2a3
#
#   - Prices per square meter of old dwellings in housing companies and numbers
#     of transactions by postal code area, yearly, 2009-2022
#     https://pxdata.stat.fi:443/PxWeb/sq/41826b15-82a9-4c83-8be6-bd77f98b31ac
#

# Read in what we've got.
incomes = pd.read_csv('data/003_12f1_2021_20230929-100110.csv',
                      encoding = 'latin1',
                      na_values = [ '0' ],
                      skiprows = [0, 1])
prices = pd.read_csv('data/001_13mu_2022_20230929-105546.csv',
                     encoding = 'latin1',
                     na_values = [ '.', '..', '...' ],
                     skiprows = [0, 1])

# %%
# A few peeks in to the data we just read.
print(f'Income/Price data shape: {incomes.shape}/{prices.shape}\n')

print(incomes.iloc[[randint(0, incomes.shape[0])]].to_string())
print(prices.iloc[[randint(0, prices.shape[0])]].to_string())

# %%
# Drop unwanted columns for ease of use later on.
incomes.drop('Information', axis = 1, inplace = True)
prices.drop([ 'Building type', 'Information' ], axis = 1, inplace = True)

# Since we do not have income data for years 2009 and 2022, we don't need pricing data for those either.
prices.drop([ '2009', '2022' ], axis = 1, inplace = True)

# Ensure column names aren't fluctuating wildly like a warp drive engine.
incomes.rename(columns = { 'Postal code area': 'Postal code' }, inplace = True)

# %%
# A few more peeks into the data, which should now appear more uniform than before.

print(f'Income/Price data shape: {incomes.shape}/{prices.shape}\n')

code = incomes.iloc[[randint(0, min(incomes.shape[0], prices.shape[0]))]]['Postal code'].values[0]
print(incomes.loc[incomes['Postal code'] == code])
print(prices.loc[prices['Postal code'] == code])

ax_incomes = incomes.plot()
ax_incomes.set_xlabel('Postal code')
ax_incomes.set_ylabel('Median Disposable Income')
_ = ax_incomes.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax_prices = prices.plot()
ax_prices.set_xlabel('Postal code')
ax_prices.set_ylabel('2 room flat sqm price')
_ = ax_prices.legend(loc='center left', bbox_to_anchor=(1, 0.5))


# %%
from pandas.plotting import autocorrelation_plot

for r in range(0, incomes.shape[0]):
  postal_code = incomes.iloc[[r]]['Postal code'].values[0]
  ax = autocorrelation_plot(incomes.iloc[[r]].T.iloc[1:])

  plt.title(postal_code)
  plt.show()

# %%
for r in range(0, prices.shape[0]):
  postal_code = prices.iloc[[r]]['Postal code'].values[0]
  ax = autocorrelation_plot(prices.iloc[[r]].T.iloc[1:])

  plt.title(postal_code)
  plt.show()


