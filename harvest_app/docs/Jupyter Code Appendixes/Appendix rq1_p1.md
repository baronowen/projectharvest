# Code appendix RQ1_P1
The code appendix for notebook Data_analyses_rq1_p1_v2.
The code in this appendix will appear in the same order as in the notebook.

## Loading conversion and postcode data
```python
# Loading in the data.
sales_data = pd.read_excel('sales_data_harvest.xlsx')

# Renaming the columns.
sales_data = sales_data.rename(columns={'Town/City': 'city',
    'Postcode': 'postcode',
    'Date': 'date',
    'Brand/Generic': 'brand',
    'Campaign': 'campaign',
    'Device': 'device',
    'Applications': 'applications',
    'Funded': 'funded',
    'Conv. %': 'conv'})
sales_dataS = sales_data.iloc[:200]

# Removing any whitespaces in the postcode column.
sales_data['postcode'] = sales_data['postcode'].str.strip()

# extracting postcode and conv columns for later use
conversions = sales_data[['postcode', 'conv']]
conversions.head()

# Loading in postcode data
postcode_coords = loadPostcodes('postcodes.csv')
postcode_coords.head()

```

## Qualification data
<b><u>Loading and merging</u></b>
```python
# Loading qualifications data
qualifications = loadCompareData('nomis_datasets/qualifications.csv', 'postcode sector', 'postcode')

# Renaming the columns
qualifications = qualifications.rename(columns={
    'All categories: Highest level of qualification': 'Total with qualifications',
    'No qualifications': 'no qualifications',
    'Highest level of qualification: Level 1 qualifications': 'level 1',
    'Highest level of qualification: Level 2 qualifications': 'level 2',
    'Highest level of qualification: Apprenticeship': 'apprenticeship',
    'Highest level of qualification: Level 3 qualifications': 'level 3',
    'Highest level of qualification: Level 4 qualifications and above': 'level 4 and over',
    'Highest level of qualification: Other qualifications': 'other'})
qualifications.head()

# Merge with postcode data
qual_joined = postcode_coords.merge(qualifications, on='postcode')
qual_joined['total pop'] = qual_joined['Total with qualifications'] + qual_joined['no qualifications']
qual_joined.head()
```
<b><u>Calculating percentage</u></b>
```python
percenQ = calcPercen(qual_joined, 'total pop', 'no qualifications', '% no qualifications')

percen2 = calcPercen(qual_joined, 'total pop', 'level 1', '% level 1')
percenQ = percenQ.merge(percen2, on='postcode')

percen2 = calcPercen(qual_joined, 'total pop', 'level 2', '% level 2')
percenQ = percenQ.merge(percen2, on='postcode')

percen2 = calcPercen(qual_joined, 'total pop', 'apprenticeship', '% apprenticeship', col1New='apprenticeship')
percenQ = percenQ.merge(percen2, on='postcode')

percen2 = calcPercen(qual_joined, 'total pop', 'level 3', '% level 3')
percenQ = percenQ.merge(percen2, on='postcode')

percen2 = calcPercen(qual_joined, 'total pop', 'level 4 and over', '% level 4 and over')
percenQ = percenQ.merge(percen2, on='postcode')

percen2 = calcPercen(qual_joined, 'total pop', 'other', '% other', col1New='other')
percenQ = percenQ.merge(percen2, on='postcode')

percenQ.head()
```
<b><u>Using `extractByPostcode()`</u></b>
```python
convPercenQ = extractByPostcode(conversions, qual_joined, 'conv')
# convPercenQ.to_csv('dataframes/convQ.csv', index=False)
convPercenQ.head()
```
<b><u>Interactive plot</u></b>
```python
# Creating widgets
widgetNumberQ = widgets.Dropdown(options=[
    'no qualifications', 'level 1', 'level 2', 'apprenticeship', 'level 3',
    'level 4 and over', 'other'],
     value='other',
     description='Qualification')

widgetPercenQ = widgets.Dropdown(options=[
    '% no qualifications', '% level 1', '% level 2', '% apprenticeship', '% level 3',
    '% level 4 and over', '% other'],
    value='% other',
    description='Percentage',
    disabled=True)

widgetFilterQ = widgets.IntSlider(value=5, min=0, max=10, step=1,
    description='Filter')

# Function to link two widgets
def transform(case):
    return {'no qualifications': '% no qualifications', 'level 1': '% level 1', 'level 2': '% level 2',
    'apprenticeship': '% apprenticeship', 'level 3': '% level 3', 'level 4 and over': '% level 4 and over',
    'other': '% other'}[case]
directional_link((widgetNumberQ, 'value'), (widgetPercenQ, 'value'), transform)

# Function to update the plot
def updatePlotQ(numberColumn, percenColumn, filterQ):
    print(numberColumn)
    if numberColumn == 'no qualifications':
        pQ.title.text = 'People with ' + numberColumn
    else:
        pQ.title.text = 'People with ' + numberColumn + ' qualifications'

    r1Q.data_source.data['color'] = qual_joined[numberColumn]
    r1Q.data_source.data['percen'] = percenQ[percenColumn]

    cQ.high = percenQ[percenColumn].max()
    cQ.low = percenQ[percenColumn].min()

    print(filterQ)

    newData = convPercenQ.loc[convPercenQ['total'] > filterQ]

    r2Q.data_source.data['lat'] = newData['latitude']
    r2Q.data_source.data['lon'] = newData['longitude']
    r2Q.data_source.data['total'] = newData['total']
    r2Q.data_source.data['total2'] = newData['total']
    r2Q.data_source.data['color'] = newData['# converted']
    r2Q.data_source.data['postcode'] = newData['postcode']
    r2Q.data_source.data['percen'] = newData['% converted']

    push_notebook(handle=tQ)

# The plots
pQ = plotMap('People with no qualification')
rQ = createSource(qual_joined, percenQ, 'total pop', 'no qualifications', '% no qualifications', divider=2500)
cQ = createColorMapper(percenQ, '% no qualifications')
tQ = createToolTips(rQ)

r1Q = pQ.circle(x='lon', y='lat', size='total', fill_color={'field': 'percen', 'transform': cQ},
    fill_alpha=0.3, source=rQ)
colorBarQ = ColorBar(color_mapper=cQ, ticker=BasicTicker(),
    label_standoff=12, border_line_color=None, location=(0,0))
pQ.add_tools(HoverTool(tooltips=tQ))
pQ.add_layout(colorBarQ, 'right')

# ---------------------------------------------------------------------------------

pQp = plotMap('Percentage converted')
rQp = createSource(convPercenQ, convPercenQ, 'total pop', '# converted', '% converted', divider=0.1)
cQp = createColorMapper(convPercenQ, '% converted')
tQp = createToolTips(rQp, label3='people', percenLabel='% converted')

r2Q = pQp.circle(x='lon', y='lat', size='total', fill_color={'field': 'percen', 'transform': cQp},
    fill_alpha=0.3, source=rQp)
colorBarQ2 = ColorBar(color_mapper=cQp, ticker=BasicTicker(),
    label_standoff=12, border_line_color=None, location=(0,0))
pQp.add_tools(HoverTool(tooltips=tQp))
pQp.add_layout(colorBarQ2, 'right')

tQ = show(row(pQ, pQp), notebook_handle=True)
interact(updatePlotQ, numberColumn=widgetNumberQ, percenColumn=widgetPercenQ, filterQ=widgetFilterQ)
```
<b><u>Calculate conversion percentage</u></b>
```python
convPercenQ.drop(['latitude', 'longitude'], axis=1, inplace=True)
convPercenQ.head()

# Calculating conversion percentage for each qualification by postcode.
newDfQC = calcPercen(convPercenQ, 'no qualifications', '# converted', '% converted no qualifications')

df2 = calcPercen(convPercenQ, 'level 1', '# converted', '% converted level 1')
newDfQC = newDfQC.merge(df2, on='postcode')

df2 = calcPercen(convPercenQ, 'level 2', '# converted', '% converted level 2')
newDfQC = newDfQC.merge(df2, on='postcode')

df2 = calcPercen(convPercenQ, 'apprenticeship', '# converted', '% converted apprenticeship', colAllNew='apprenticeship')
newDfQC = newDfQC.merge(df2, on='postcode')

df2 = calcPercen(convPercenQ, 'level 3', '# converted', '% converted level 3')
newDfQC = newDfQC.merge(df2, on='postcode')

df2 = calcPercen(convPercenQ, 'level 4 and over', '# converted', '% converted level 4 and over')
newDfQC = newDfQC.merge(df2, on='postcode')

df2 = calcPercen(convPercenQ, 'other', '# converted', '% converted other', colAllNew='other')
newDfQC = newDfQC.merge(df2, on='postcode')

newDfQC.head()
```
<b><u>Plot with average conversion percentage</u></b>
```python
dictQ = newDfQC.mean()
dictQ = round(dictQ, 3)

dictQ = dictQ.to_dict()
dictQ['no'] = dictQ.pop('% converted no qualifications')
dictQ['level 1'] = dictQ.pop('% converted level 1')
dictQ['level 2'] = dictQ.pop('% converted level 2')
dictQ['apprenticeship'] = dictQ.pop('% converted apprenticeship')
dictQ['level 3'] = dictQ.pop('% converted level 3')
dictQ['level 4 +'] = dictQ.pop('% converted level 4 and over')
dictQ['other'] = dictQ.pop('% converted other')

names = list(dictQ.keys())
values = list(dictQ.values())

plt.figure()
plt.title('% converted qualifications')
plt.plot(names, values, marker='o', markerfacecolor='red')
plt.xlabel('Qualification level')
plt.ylabel('average conversion %')
for i,j in zip(names, values):
    plt.annotate(str(j), xy=(i,j), xytext=(-5,5), textcoords='offset points')
```

## Occupation data
<b><u>Loading and merging</u></b>
```python
# Loading occupation data
occupation = loadCompareData('nomis_datasets/occupation.csv', 'postcode sector', 'postcode')

# Renaming the columns
occupation = occupation.rename(columns={
    '1. Managers, directors and senior officials': '1 managers/directors',
    '2. Professional occupations': '2 professionals',
    '3. Associate professional and technical occupations': '3 technical professional',
    '4. Administrative and secretarial occupations': '4 administrative',
    '5. Skilled trades occupations': '5 skilled trades',
    '6. Caring, leisure and other service occupations': '6 service',
    '7. Sales and customer service occupations': '7 sales and customer service',
    '8. Process plant and machine operatives': '8 process/machine operatives',
    '9. Elementary occupations': '9 elementary'})

occupation['10 total'] = occupation['1 managers/directors'] + occupation['2 professionals'] +
occupation['3 technical professional'] + occupation['4 administrative'] + occupation['5 skilled trades'] +
occupation['6 service'] +occupation['7 sales and customer service'] +
occupation['8 process/machine operatives'] + occupation['9 elementary']

occupation.head()

# Merge with postcode data
occupation_joined = postcode_coords.merge(occupation, on='postcode')
occupation_joined.head()
```
<b><u>Calculating percentage</u></b>
```python
percenO = calcPercen(dfName=occupation_joined, colAll='10 total',
    col1='1 managers/directors', newColName='% 1 managers/directors')

df2 = calcPercen(occupation_joined, '10 total', '2 professionals', '% 2 professionals')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '3 technical professional', '% 3 technical professional')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '4 administrative', '% 4 administrative')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '5 skilled trades', '% 5 skilled trades')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '6 service', '% 6 service')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '7 sales and customer service', '% 7 sales and customer service')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '8 process/machine operatives', '% 8 process/machine operatives')
percenO = percenO.merge(df2, on='postcode')

df2 = calcPercen(occupation_joined, '10 total', '9 elementary', '% 9 elementary')
percenO = percenO.merge(df2, on='postcode')

percenO.head()
```
<b><u>Using `extractByPostcode()`</u></b>
```python
convPercenO = extractByPostcode(conversions, occupation_joined, 'conv')
# convPercenO.to_csv('dataframes/convO.csv', index=False)
convPercenO.head()
```
<b><u>Interactive plot</u></b>
```python
# Creating the widgets
widgetNumberO = widgets.Dropdown(options=[
    '1 managers/directors', '2 professionals', '3 technical professional',
    '4 administrative', '5 skilled trades', '6 service',
    '7 sales and customer service', '8 process/machine operatives', '9 elementary'],
    value='1 managers/directors',
    description='Occupation')

widgetPercenO = widgets.Dropdown(options=[
    '% 1 managers/directors', '% 2 professionals', '% 3 technical professional',
    '% 4 administrative', '% 5 skilled trades', '% 6 service',
    '% 7 sales and customer service', '% 8 process/machine operatives', '% 9 elementary'],
    value='% 1 managers/directors',
    description='Percentage',
    disabled=True)

widgetFilterO = widgets.IntSlider(value=5, min=0, max=10, step=1,
    description='Filter',
    disabled=False)

# Function to link two widgets
def transformO(case):
    return {'1 managers/directors': '% 1 managers/directors', '2 professionals': '% 2 professionals',
    '3 technical professional': '% 3 technical professional',
    '4 administrative': '% 4 administrative', '5 skilled trades': '% 5 skilled trades',
    '6 service': '% 6 service', '7 sales and customer service': '% 7 sales and customer service',
    '8 process/machine operatives': '% 8 process/machine operatives', '9 elementary': '% 9 elementary'}[case]
directional_link((widgetNumberO, 'value'), (widgetPercenO, 'value'), transformO)

# Function to update the plot
def updatePlotO(numberColumn, percenColumn, filterO):
    print(numberColumn)
    pO.title.text = numberColumn

    r1O.data_source.data['color'] = occupation_joined[numberColumn]
    r1O.data_source.data['percen'] = percenO[percenColumn]

    cO.high = percenO[percenColumn].max()
    cO.low = percenO[percenColumn].min()

    newData = convPercenO.loc[convPercenO['total'] > filterO]

    r2O.data_source.data['lat'] = newData['latitude']
    r2O.data_source.data['lon'] = newData['longitude']
    r2O.data_source.data['total'] = newData['total']
    r2O.data_source.data['total2'] = newData['total']
    r2O.data_source.data['color'] = newData['# converted']
    r2O.data_source.data['postcode'] = newData['postcode']
    r2O.data_source.data['percen'] = newData['% converted']

    push_notebook(handle=tO)

# The plots
pO = plotMap('1 managers/directors')
rO = createSource(occupation_joined, percenO, '10 total', '1 managers/directors', '% 1 managers/directors', divider=2500)
cO = createColorMapper(percenO, '% 1 managers/directors')
tO = createToolTips(rO)

r1O = pO.circle(x='lon', y='lat', size='total', fill_color={'field': 'percen', 'transform': cO},
                fill_alpha=0.3, source=rO)
colorBarO = ColorBar(color_mapper=cO, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
pO.add_tools(HoverTool(tooltips=tO))
pO.add_layout(colorBarO, 'right')

# -------------------------------------------------------------------------------------------------------------------------

pOp = plotMap('Percentage converted')
rOp = createSource(convPercenO, convPercenO, 'total', '# converted', '% converted', divider=1)
cOp = createColorMapper(convPercenO, '% converted')
tOp = createToolTips(rOp, label3='People who showed interest', percenLabel='% of people who converted')

r2O = pOp.circle(x='lon', y='lat', size='total', fill_color={'field': 'percen', 'transform': cOp},
                fill_alpha=0.3, source=rOp)
colorBarO2 = ColorBar(color_mapper=cOp, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
pOp.add_tools(HoverTool(tooltips=tOp))
pOp.add_layout(colorBarO2, 'right')

tO = show(row(pO, pOp), notebook_handle=True)
interact(updatePlotO, numberColumn=widgetNumberO, percenColumn=widgetPercenO, filterO=widgetFilterO)
```
<b><u>Calculate conversion percentage</u></b>
```python
convPercenO.drop(['latitude', 'longitude'], axis=1, inplace=True)
convPercenO.head()

# Calculating conversion percentage for each qualification by postcode.
newDfO = calcPercen(convPercenO, '10 total', '# converted', '% converted total')
df2 = calcPercen(convPercenO, '1 managers/directors', '# converted', '% converted 1 managers')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '2 professionals', '# converted', '% converted 2 professionals')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '3 technical professional', '# converted', '% converted 3 technical professional')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '4 administrative', '# converted', '% converted 4 administrative')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '5 skilled trades', '# converted', '% converted 5 skilled trades')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '6 service', '# converted', '% converted 6 service')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '7 sales and customer service', '# converted', '% converted 7 sales and customer service')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '8 process/machine operatives', '# converted', '% converted 8 process/machine operatives')
newDfO = newDfO.merge(df2, on='postcode')

df2 = calcPercen(convPercenO, '9 elementary', '# converted', '% converted 9 elementary')
newDfO = newDfO.merge(df2, on='postcode')

newDfO.sort_values(by='postcode')
# newDfO.to_csv('convPercenO.csv', index=False)
# newDfA.loc[newDfA['postcode'] == 'CR0']
newDfO.head()
```
<b><u>Plot with average conversion percentage</u></b>
```python
dictO = newDfO.mean()
dictO = round(dictO, 3)

dictO = dictO.to_dict()
dictO['total'] = dictO.pop('% converted total')
del dictO['total']
dictO['managers'] = dictO.pop('% converted 1 managers')
dictO['professionals'] = dictO.pop('% converted 2 professionals')
dictO['technical professional'] = dictO.pop('% converted 3 technical professional')
dictO['administrative'] = dictO.pop('% converted 4 administrative')
dictO['skilled trades'] = dictO.pop('% converted 5 skilled trades')
dictO['service'] = dictO.pop('% converted 6 service')
dictO['sales/customer service'] = dictO.pop('% converted 7 sales and customer service')
dictO['process/machine operatives'] = dictO.pop('% converted 8 process/machine operatives')
dictO['elementary'] = dictO.pop('% converted 9 elementary')

names = list(dictO.keys())
values = list(dictO.values())

plt.figure(figsize=(15,10))
plt.title('% converted occupation')
plt.plot(names, values, marker='o', markerfacecolor='red')
plt.xlabel('Occupation type')
plt.ylabel('Average conversion %')
for i,j in zip(names, values):
    plt.annotate(str(j), xy=(i,j), xytext=(-5,10), textcoords='offset points')
```

## Housing type data
<b><u>Loading and merging</u></b>
```python
# Loading occupation data
housing_type = loadCompareData('nomis_datasets/housing type.csv', 'postcode sector', 'postcode')

# Renaming the columns
housing_type = housing_type.rename(columns={
    'Unshared dwelling': 'unshared dwelling',
    'Shared dwelling: Two household spaces': 'shared dw 2 spaces',
    'Shared dwelling: Three or more household spaces': 'shared dw =>3',                                        
    'Whole house or bungalow: Detached': 'detached house',
    'Whole house or bungalow: Semi-detached': 'semi-detached house',
    'Whole house or bungalow: Terraced (including end-terrace)': 'terraced house',
    'Flat, maisonette or apartment: Purpose-built block of flats or tenement': 'flat/apartment',
    'Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)': 'flat/apartment converted',
    'Flat, maisonette or apartment: In a commercial building': 'flat/apartment commercial',
    'Caravan or other mobile or temporary structure': 'caravan'})

housing_type['totalH'] = housing_type['detached house'] + housing_type['semi-detached house'] +
housing_type['terraced house'] + housing_type['flat/apartment'] + housing_type['flat/apartment converted'] +
housing_type['flat/apartment commercial'] + housing_type['caravan']

housing_type.head()

# Merge with postcode data
housing_joined = postcode_coords.merge(housing_type, on='postcode')
housing_joined.head()
```
<b><u>Calculating percentage</u></b>
```python
percenH = calcPercen(dfName=housing_joined, colAll='totalH', col1='detached house',
newColName='% detached house', colAllNew='totalH')

df2 = calcPercen(housing_joined, 'totalH', 'semi-detached house', '% semi-detached house', colAllNew='totalH')
percenH = percenH.merge(df2, on='postcode')

df2 = calcPercen(housing_joined, 'totalH', 'terraced house', '% terraced house', colAllNew='totalH')
percenH = percenH.merge(df2, on='postcode')

df2 = calcPercen(housing_joined, 'totalH', 'flat/apartment', '% flat/apartment', colAllNew='totalH')
percenH = percenH.merge(df2, on='postcode')

df2 = calcPercen(housing_joined, 'totalH', 'flat/apartment converted', '% flat/apartment converted', colAllNew='totalH')
percenH = percenH.merge(df2, on='postcode')

df2 = calcPercen(housing_joined, 'totalH', 'flat/apartment commercial', '% flat/apartment commercial', colAllNew='totalH')
percenH = percenH.merge(df2, on='postcode')

df2 = calcPercen(housing_joined, 'totalH', 'caravan', '% caravan', col1New='caravan', colAllNew='totalH')
percenH = percenH.merge(df2, on='postcode')

percenH.head()
```
<b><u>Using `extractByPostcode()`</u></b>
```python
convPercenH = extractByPostcode(conversions, housing_joined, 'conv')
# convPercenH.to_csv('dataframes/convHtype.csv', index=False)
convPercenH.head()
```
<b><u>Interactive plot</u></b>
```python
# Creating the widgets
widgetNumberH = widgets.Dropdown(options=[
    'detached house', 'semi-detached house', 'terraced house', 'flat/apartment',
    'flat/apartment converted', 'flat/apartment commercial', 'caravan'],
    value='detached house',
    description='Housing type')

widgetPercenH = widgets.Dropdown(options=[
    '% detached house', '% semi-detached house', '% terraced house',
    '% flat/apartment', '% flat/apartment converted', '% flat/apartment commercial',
    '% caravan'],
    value='% detached house',
    description='Percentage',
    disabled=True)
widgetFilterH = widgets.IntSlider(value=5, min=0, max=10, step=1,
    description='Filter',
    disabled=False)

# Function to link two widgets
def transformH(case):
    return {'detached house': '% detached house', 'semi-detached house': '% semi-detached house',
    'terraced house': '% terraced house', 'flat/apartment': '% flat/apartment',
    'flat/apartment converted': '% flat/apartment converted',
    'flat/apartment commercial': '% flat/apartment commercial', 'caravan': '% caravan'}[case]
directional_link((widgetNumberH, 'value'), (widgetPercenH, 'value'), transformH)

# Function to update the plot
def updatePlotH(numberColumn, percenColumn, filterH):
    print(numberColumn)
    pH.title.text = numberColumn

    r1H.data_source.data['color'] = housing_joined[numberColumn]
    r1H.data_source.data['percen'] = percenH[percenColumn]

    cH.high = percenH[percenColumn].max()
    cH.low = percenH[percenColumn].min()

    print(filterH)

    newData = convPercenH.loc[convPercenH['total'] > filterH]

    r2H.data_source.data['lat'] = newData['latitude']
    r2H.data_source.data['lon'] = newData['longitude']
    r2H.data_source.data['total'] = newData['total']
    r2H.data_source.data['total2'] = newData['total']
    r2H.data_source.data['color'] = newData['# converted']
    r2H.data_source.data['postcode'] = newData['postcode']
    r2H.data_source.data['percen'] = newData['% converted']

    push_notebook(handle=tH)

# The plots
pH = plotMap('Detached houses')
rH = createSource(housing_joined, percenH, 'totalH', 'detached house', '% detached house', divider=2500)
cH = createColorMapper(percenH, '% detached house')
tH = createToolTips(rH)

r1H = pH.circle(x='lon', y='lat', size='total', fill_color={'field': 'percen', 'transform': cH},
              fill_alpha=0.3, source=rH)
colorBarH = ColorBar(color_mapper=cH, ticker=BasicTicker(),
                   label_standoff=12, border_line_color=None, location=(0,0))
pH.add_tools(HoverTool(tooltips=tH))
pH.add_layout(colorBarH, 'right')

# ----------------------------------------------------------------------------------------------------------

pHp = plotMap('Percentage converted')
rHp = createSource(convPercenH, convPercenH, 'total', '# converted', '% converted', divider=1)
cHp = createColorMapper(convPercenH, '% converted')
tHp = createToolTips(rHp, label3='People who showed interest', percenLabel='% of people who converted')

r2H = pHp.circle(x='lon', y='lat', size='total', fill_color={'field': 'percen', 'transform': cHp},
                fill_alpha=0.3, source=rHp)
colorBarH2 = ColorBar(color_mapper=cHp, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
pHp.add_tools(HoverTool(tooltips=tHp))
pHp.add_layout(colorBarH2, 'right')

tH = show(row(pH, pHp), notebook_handle=True)
interact(updatePlotH, numberColumn=widgetNumberH, percenColumn=widgetPercenH, filterH=widgetFilterH)
```
<b><u>Calculate conversion percentage</u></b>
```python
convPercenH.drop(['latitude', 'longitude'], axis=1, inplace=True)
convPercenH.head()

# Calculating conversion percentage for each qualification by postcode.
newDfH = calcPercen(convPercenH, 'totalH', '# converted', '% converted total', colAllNew='totalH')
df2 = calcPercen(convPercenH, 'detached house', '# converted', '% converted detached house')
newDfH = newDfH.merge(df2, on='postcode')

df2 = calcPercen(convPercenH, 'semi-detached house', '# converted', '% converted semi-detached')
newDfH = newDfH.merge(df2, on='postcode')

df2 = calcPercen(convPercenH, 'terraced house', '# converted', '% converted terraced')
newDfH = newDfH.merge(df2, on='postcode')

df2 = calcPercen(convPercenH, 'flat/apartment', '# converted', '% converted flat/apartment')
newDfH = newDfH.merge(df2, on='postcode')

df2 = calcPercen(convPercenH, 'flat/apartment converted', '# converted', '% converted flat/apartment converted')
newDfH = newDfH.merge(df2, on='postcode')

df2 = calcPercen(convPercenH, 'flat/apartment commercial', '# converted', '% converted flat/apartment commercial')
newDfH = newDfH.merge(df2, on='postcode')

df2 = calcPercen(convPercenH, 'caravan', '# converted', '% converted caravan', colAllNew='caravan')
newDfH = newDfH.merge(df2, on='postcode')

newDfH.sort_values(by='postcode')
# newDfH.to_csv('convPercenHtype.csv', index=False)
# newDfH.loc[newDfA['postcode'] == 'CR0']
newDfH.head()
```
<b><u>Plot with average conversion percentage</u></b>
```python
dictHt = newDfH.mean()
dictHt = round(dictHt, 3)

dictHt = dictHt.to_dict()
dictHt['total'] = dictHt.pop('% converted total')
del dictHt['total']
dictHt['detached'] = dictHt.pop('% converted detached house')
dictHt['semi-detached'] = dictHt.pop('% converted semi-detached')
dictHt['terraced'] = dictHt.pop('% converted terraced')
dictHt['flat/apartment'] = dictHt.pop('% converted flat/apartment')
dictHt['flat converted'] = dictHt.pop('% converted flat/apartment converted')
dictHt['flat commercial'] = dictHt.pop('% converted flat/apartment commercial')
dictHt['caravan'] = dictHt.pop('% converted caravan')

names = list(dictHt.keys())
values = list(dictHt.values())

plt.figure(figsize=(10,7))
plt.title('% converted housing type')
plt.plot(names, values, marker='o', markerfacecolor='red')
plt.xlabel('Housing type')
plt.ylabel('Average conversion %')
for i,j in zip(names, values):
    plt.annotate(str(j), xy=(i,j), xytext=(-5,5), textcoords='offset points')
```
