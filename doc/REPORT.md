# DATA11001: Mini Project Report

Project team: Michaela Söderholm, Sami Laine, and Samu Syrjänen.

## Motivation Behind the Mini Project and the Initial Plan

In real estate a common profit maximisation strategy is to try and make purchaces
in an area which is about to gentrify, then renovate properties bought to sell
them once gentrification is in full swing. The strategy has been shown to produce
increase profits by several percentage points over purchaces made without considering
gentrification.

Thus, a real estate speculator faces the following problem of finding areas
about to gentrify. Though statistical data of e.g. incomes and housing prices is
available, shifting through all the timeseries found in the data is not only
time consuming but also far from what a real estate speculator should be doing,
which is looking at properties, hiring crews to renovate what already has been
bought, and so on.

One solution to this problem is to digest available statistical data and produce
a visualisation, a map, on which each city district or similar divisions of the
area are show in terms of how gentrified they might be in the near future. The
initial plan was to "somehow find suitable income and other data, and then produce
a coloured map showing how gentrified each city district might be".

## Reflections on the Initial Plan

The initial plan turned out to be workable, as several suitable data sets were
found to be openly available. When it came to data sets, the only problem seemed
to be the problem of abundance: For example historical time series of household
and personal taxable income were found from multiple data providers, one of which
partitioned Helsinki by city district and another doing partition by postal code
areas. Another problem was to decide which data sets were the most relevant.
For instance, income data obviously is crucial, and housing price data probably
is important, but how important it is to know the average household size
when taking into account how the affluent usually live in more spacious settings
than the poor?

After some back and forth, the team settled with producing a minimum viable
product with either one or two data sets. It'd be much easier to add more
data sets later once there's something working to improve upon.

## And Towards a Production Quality Delivery

Considering the scope and the amount of time expected to be put into a mini
project, some corners had to be cut and the result is not what one might call
a production quality delivery. However, the mini project shows that the concept
is not entirely inusable (or inutile), and with the following improvements
the result could be improved to be more than a proof of concept:

* Inflation together with its effects on incomes and real estate prices should
be taken into account when computing predictions (incomes and prices rise in tandem
with inflation, and increases equivalent to general inflation do not indicate
gentrification).
* The backend should fetch data automatically instead of relying on a human fetching the data.
* More data sets should be used. For example, statistics about health service usage might help
as it's a known fact how the poor are more and more often sick than the rich.

## Technical Description

### Data Collection

The main data collection tool used was actually not a data collection tool at all.
In order to locate data sets which might be helpful in the mini project, simple
Google searches were used to locate suitable data sets. The team decided to use
only two data sets, one describing historical income fluctuations and another
describing historical real estate prices.

Once the suitable data sets were identified, they (see [../data/README.md](../data/README.md)),
they were downloaded manually. Though it could've been possible to automate this step,
it seemed unnecessary as the mini project is presumed to be a proof of concept instead of
"a fully finished production quality delivery"; so, it seemed like time would be better
spent on other aspects of the mini project.

### Preprocessing and Machine Learning

It turned out that a GeoJSON featurecollection describing borders of postal code areas
in Helsinki was not available, so instead a shapefile containing similar information was
used. The shapefile was converted into a GeoJSON featurecollection using a Python Library
[GeoPandas](https://geopandas.org/), which offered a ready-to-use function `.to_json()`
and there wasn't more to it.

Other data sets containing income and real estate price information came from
[Statistics Finland](https://stat.fi/index_en.html). Since Statistics Finland is the national
statistics institute in Finland, the data was in good overall condition right from the beginning.
However, nothing is perfect, and two minor preprocessing tasks using a Python library
[Pandas](https://pandas.pydata.org/) had to be done.
First, one of the data sets called postal codes "postal codes" whereas the other called them
"postal code areas"; thus, a column had to be renamed in one data set.
Second, in both data sets postal codes were mixed with human readable names of the postal code
areas; so, for example "00140  Kaivopuisto - Ullanlinna (Helsinki)" had to be turned into
"00140" (the rest got split into its own column just to keep things easily readable for us humans
during later programming stages).

As suggested by one of the teaching assistants, in order to produce a prediction of 
gentrification for each postal code area, first an
[autoregressive integrated moving average model](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average)
(ARIMA) model was trained separately on historical income and real estate price data
from each postal code area. Then each model was used to produce two predictions,
one for future income levels and another for future real estate prices, for each
postal code area. Finally, the two predictions were used to compute percentage
difference between the last item in each time series in each postal code area,
and the mean of the percentages was taken to be a "gentrification percentage score".
Since the value thus obtained lands on the interval [0,100], it could
be used easily to change opaqueness of colouring on the visualisation (values
for opacity in Cascading Style Sheets being on the interval [0,1]).

### Visualisations and Communication of Results

In order to communicate results to the intended target audience, a single web page
with an interactive map was produced. The map is coloured using two colours, blue and
red, in varying hues: Colours indicate whether an area is predicted to be less (blue)
or more (red) gentrified in the future and the hue indicates how big the change
is predicted to be.

The technical implementation relies heavily on [Leaflet](https://leafletjs.com/),
a JavaScript library providing everything needed to build a mapping application.
In order to implement a map showing gentrification predictions, the team only needed
to find a GeoJSON featurecollection with postal code area borders and produce
a JSON file with gentrification predictions. The GeoJSON and JSON data are first
read using
[the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
and once read, they're mashed together to produce a map communicating the
results.

### Building the Platform

Because the end result for the intended target audience is a single web page with
an interactive map, there really was no platform to be built. All code and data
for the mini project was hosted in a git repository, so publishing the web page
with [GitHub Pages](https://pages.github.com/) was a natural, and easy, solution.
