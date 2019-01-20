# Code appendix Jupyter functions.

## Code in `datasets\functions\functions.py`
<b><u>Imports and variables</u></b>
```python
import numpy as np
import pandas as pd

from traitlets import directional_link

from bokeh.io import push_notebook, output_notebook, show
from bokeh.models import GMapOptions, BasicTicker, ColorBar,
     ColumnDataSource, SaveTool, HoverTool
from bokeh.plotting import gmap, figure
from bokeh.models.mappers import ColorMapper, LinearColorMapper
from bokeh.palettes import *
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.models.widgets import *

# where to start the map.
map_options = GMapOptions(lat=52.9740, lng=-2.9198, map_type='roadmap', zoom=6)
api_key = 'AIzaSyDF_wubdInFvDGUVIHRUASEbCn8prrv4eY' # Replace key with your own.
```
<b><u>PlotMap function</u></b>
```python
def plotMap(plotTitle, api_key=api_key, map_options=map_options,
            plotWidth=400, plotHeight=500):

    plot = gmap(api_key, map_options, title=plotTitle,
        plot_width=plotWidth, plot_height=plotHeight,
        toolbar_location='above', toolbar_sticky=False)
    plot.add_tools(SaveTool())

    return plot;
```
<b><u>CreateSource function</u></b>
```python
def createSource(dfName, dfNamePercen, totalColumn, numberColumn,
    percenColumn,
    postcodeColumn='postcode', latColumn='latitude', lonColumn='longitude',
    divider=1):
    """
    Create the datasource for a glyph to use.
    """

    data = ColumnDataSource(dict(lat=dfName[latColumn],
        lon=dfName[lonColumn],
        total=dfName[totalColumn]/divider,
        total2=dfName[totalColumn],
        color=dfName[numberColumn],
        postcode=dfName[postcodeColumn],
        percen=dfNamePercen[percenColumn]))
    return data;
```
<b><u>CreateToolTips function</u></b>
```python
def createToolTips(data, label3='Number of people', percenLabel='% of people'):
    """
    Creates tooltips which show when hovering over a datapoint in a plotself.
    This function is designed to create the tooltips for a map plotself.
    Parameters
    -----------
    data : pd.DataFrame
        The data source which to tie the tooltips toself.
    label3 : string
        The string you want the third label to showself.
    percenLabel: string
        The string you want the fourth(percent) label to show.
    Returns
    -------
    toolTips : array
        An array with labels and its valuesself.
    """

    toolTips = [('Postcode', '@postcode'),
        ('Total people', '@total2'),
        (label3, '@color'),
        (percenLabel, '@percen %')]
    return toolTips;
```
<b><u>CreateColorMapper function</u></b>
```python
def createColorMapper(dfName, percenColumn):
    """
    Creates a color_mapper
    Parameters
    ----------
    dfName : pd.DataFrame
        The name of the dataframe with percenColumn
    percenColumn : string
        The name of the column you want the color bar to be based onself.
    Returns
    -------
    color_mapper : LinearColorMapper
        An object that contains the color_mapper which is used in a ColorBar
    """
    color_mapper = LinearColorMapper(palette=Plasma10,
        low=dfName[percenColumn].min(),
        high=dfName[percenColumn].max())
    return color_mapper;
```
<b><u>CalcPercen function</u></b>
```python
def calcPercen(dfName, colAll, col1, newColName, colAllNew='_2', col1New='_3'):
    """
    This function calculates the conversion rate/percentage for each postcode.
    Parameters
    ----------
    dfName : pd.DataFrame
        the dataframe used to retrieve the data.
        Make sure all data necessary is in this dataframe.
    colAll : string
        the total number by postcode of 1 type.
    col1 : string
        the number by postcode that converted.
    newColName : string
        the new name for the column.
    colAllNew : string (optional)
        the name of the column within the loop if there
        is one or more space in
        the column name of the dataframe.
    col1New : string (optional)
        the name of the column within the loop if there
        is one or more space in
        the column name of the dataframe.
    Returns
    -------
    temp : pandas.DataFrame
        The caculated data.
    """

    temp = dfName[['postcode', colAll, col1]]
    tempDict = {}

    for row in temp.itertuples():
        postcode = getattr(row, 'postcode')
        x = getattr(row, col1New)
        y = getattr(row, colAllNew)

        if x == 0 or y == 0:
            z = 0
        else:
            z = (x/y) * 100

        tempDict[postcode] = z

    temp[newColName] = temp['postcode'].map(tempDict)
    temp = temp.drop([colAll, col1], axis=1)

    return temp;
```
<b><u>ExtractByPostcode function</u></b>
```python
def extractByPostcode(conversionData, compareToData, conversionColumn,
    postcodeColumn='postcode',
    colNameTotal='total', colNameConvert='# converted'):
    """
    Extracts the total # of people who showed interest,
    # of people who converted, and percentage
    of people who converted.
    Keep in mind that the 2 dataframes both
    need to have a column named 'postcode'.
    Parameters
    -----------
    conversionData : pd.DataFrame
        The dataframe with the conversion data
    compareToData : pd.DataFrame
        The dataframe with the data to compare with
    conversionColumn : string
        The column name with the conversion data
    Returns
    -------
    temp : pd.DataFrame
        A new dataframe with the extra columns
    """
    temp = pd.DataFrame()
    if isinstance(conversionColumn, str) and isinstance(postcodeColumn, str):
        if isinstance(colNameTotal, str) and isinstance(colNameConvert, str):
            joined = conversionData.merge(compareToData, on='postcode')
            total = joined[postcodeColumn].value_counts()
            total = total.to_frame().reset_index()
            total = total.rename(columns={'index': 'postcode',
                postcodeColumn: colNameTotal})

            converted = joined[[postcodeColumn, conversionColumn]]

            converted = converted.loc[converted[conversionColumn] > 0]
            converted = converted[postcodeColumn].value_counts()
            converted = converted.to_frame().reset_index()
            converted = converted.rename(columns={'index': 'postcode',
                postcodeColumn: colNameConvert})

            newDf = total.merge(converted, on=postcodeColumn, how='outer')
            print("newDf: ", newDf.shape)
            print('newDf: ', newDf)
            newDf["difference"] = (newDf[colNameTotal] - newDf[colNameConvert])
            newDf["% converted"] = (newDf[colNameConvert] / newDf[colNameTotal]) * 100


            temp = newDf.merge(compareToData, on=postcodeColumn, how='inner')
            return temp;
        else:
            print('Make sure you us a string for'
            'colNameTotal and colNameConvert')
            return temp;
    else:
        print('Make sure you us a string for '
        'conversionColumn and postcodeColumn')
        return temp;
```
<b><u>CutDataFrame function</u></b>
```python
def cutDataFrame(dfName, toCluster, nBins, *labels):
    """
    Function to cluster a dataframe manually.
    Parameters
    ----------
    dfName : pd.DataFrame
        The dataframe containing toCluster.
    toCluster : string
        The name of the column that is to be clustered.
    nBins : int
        The number of bins one whishes to create.
    *labels : string
        The labels one wants for the clusters. Number of labels HAS
        to be equal to nBins.
    Returns
    -------
    temp : pd.DataFrame
        A new dataframe with two extra columns
        containing the cluster labels
        and the labels encoded.
    """
    if isinstance(nBins, int):
        temp = dfName[:]
        label = 'label'

        if len(labels) == int(nBins):

            temp[label] = pd.cut(temp[toCluster], nBins, labels=labels)

        else:
            print('number of labels do not match number of Bins. '
              '\nnBins = ', nBins,
              '\nNumber of labels = ', len(labels))

        temp[label] = temp[label].astype('category')
        temp['cat'] = temp[label].cat.codes

        return temp;
    else:
        print('Give a number for nBins!')
```

## Code in `datasets\functions\dataLoading.py`
<b><u>LoadPostcodes function</u></b>
```python
def loadPostcodes(postcode_path):
    """
    Load in a file which contains postcode coordinates.
    Parameters
    -----------
    postcode_path : string
        the path that leads to the file with postcodes and coordinates
    Returns
    -------
    coords : pd.DataFrame
        a dataframe containing postcodes and coordinates
    """
    temp = pd.read_csv(postcode_path)
    temp['postcode'] = temp['postcode'].str.strip()

    coords = temp[['postcode', 'latitude', 'longitude']]
    return coords;
```
<b><u>LoadCompareData function</u></b>
```python
def loadCompareData(data_path, postcodeOld, postcodeNew):
    """
    Make sure the data is in csv format.
    """
    temp = pd.read_csv(data_path)
    temp = temp.rename(columns={postcodeOld: postcodeNew})

    temp[postcodeNew] = temp[postcodeNew].str.split('\s+').str[0]

    temp = temp.groupby([postcodeNew]).sum().reset_index()

    temp[postcodeNew] = temp[postcodeNew].str.strip()

    return temp;
```
