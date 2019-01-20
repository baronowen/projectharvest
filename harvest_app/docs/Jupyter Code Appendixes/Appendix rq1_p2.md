# Code appendix RQ1_P2
The code appendix for notebook `Data_analyses_rq1_p2`.
The code in this appendix will appear in the same order as in the notebook.

## Loading conversion and postcode data
```python
# Loading in the conversion data.
data = pd.read_excel('Mob Group_full_Salesforce_Leads_Report.xlsx')

# Drop columns that are of no use or not relevant.
data = data.drop(['Lead_Ref_Number', 'City',
    'Sales_Region_Area', 'PostalCode', 'Short_Postcode',
    'Sales_Advisors_Name'], axis=1)
print(data.shape)

# Rename columns.
dataMobG = data.rename(columns={
    'Contract_sign_date': 'contract_sign_date',
    'Brand': 'brand',
    'GA_User_ID': 'userId',
    'Postcode_District': 'postcode',
    'Price_agreed': 'priceAgreed',
    'Interested_In?': 'interestedIn',
    'Product_Ordered': 'orderedProduct',
    'Who_for': 'forWho',
    'Ailments': 'ailments',
    'Customer_needs': 'customerNeeds'})

# Drop rows where the following columns ALL have NaN values.
dataMobG = dataMobG.dropna(subset=['interestedIn',
    'orderedProduct', 'Product_Ordered_Type', 'forWho',
    'ailments', 'customerNeeds'], how='all')

# Convert userId to string.
dataMobG['userId'] = dataMobG['userId'].astype(str)

# Replace NaN values in priceAgreed with 0
dataMobG['priceAgreed'].fillna(0, inplace=True)
dataMobG.head()

# Loading in postcode data
postcode_coords = loadPostcodes('postcodes.csv')
postcode_coords.head()
```
## Age structure data
<b><u> Loading and merging</u></b>
```python
age_structure = loadCompareData('nomis_datasets/age_structure.csv',
    'postcode sector', 'postcode')

# Reducing the amount of columns.
age_structure['0 to 15'] = age_structure['Age 0 to 4'] +
    age_structure['Age 5 to 7'] + age_structure['Age 8 to 9'] +
    age_structure['Age 10 to 14'] + age_structure['Age 15']
age_structure.drop(['Age 0 to 4', 'Age 5 to 7',
    'Age 8 to 9', 'Age 10 to 14', 'Age 15'], axis=1, inplace=True)

age_structure['16 to 19'] = age_structure['Age 16 to 17'] +
    age_structure['Age 18 to 19']
age_structure.drop(['Age 16 to 17',
    'Age 18 to 19'], axis=1, inplace=True)

age_structure['20 to 29'] = age_structure['Age 20 to 24'] +
  age_structure['Age 25 to 29']
age_structure.drop(['Age 20 to 24',
    'Age 25 to 29'], axis=1, inplace=True)

age_structure['30 to 44'] = age_structure['Age 30 to 44']
age_structure.drop(['Age 30 to 44'], axis=1, inplace=True)

age_structure['45 to 64'] = age_structure['Age 45 to 59'] +
  age_structure['Age 60 to 64']
age_structure.drop(['Age 45 to 59',
    'Age 60 to 64'], axis=1, inplace=True)

age_structure['65 to 84'] = age_structure['Age 65 to 74'] +
  age_structure['Age 75 to 84']
age_structure.drop(['Age 65 to 74',
    'Age 75 to 84'], axis=1, inplace=True)

age_structure['85 and over'] = age_structure['Age 85 to 89'] +
  age_structure['Age 90 and over']
age_structure.drop(['Age 85 to 89',
    'Age 90 and over'], axis=1, inplace=True)

age_structure = age_structure.rename(columns={
    'All usual residents': 'total residents'})
age_structure.head()

# Merge with postcode  data
age_joined = postcode_coords.merge(age_structure,
    left_on='postcode', right_on='postcode')
age_joined.head()
```
<b><u>Calculating percentage</u></b>
```python
percenA = calcPercen(dfName=age_joined, colAll='total residents',
    col1='0 to 15', newColName='% 0 to 15')

percenA2 = calcPercen(age_joined, 'total residents',
    '16 to 19', '% 16 to 19')
percenA = percenA.merge(percenA2, on='postcode')

percenA2 = calcPercen(age_joined, 'total residents',
    '20 to 29', '% 20 to 29')
percenA = percenA.merge(percenA2, on='postcode')

percenA2 = calcPercen(age_joined, 'total residents',
    '30 to 44', '% 30 to 44')
percenA = percenA.merge(percenA2, on='postcode')

percenA2 = calcPercen(age_joined, 'total residents',
    '45 to 64', '% 45 to 64')
percenA = percenA.merge(percenA2, on='postcode')

percenA2 = calcPercen(age_joined, 'total residents',
    '65 to 84', '% 65 to 84')
percenA = percenA.merge(percenA2, on='postcode')

percenA2 = calcPercen(age_joined, 'total residents',
    '85 and over', '% 85 and over')
percenA = percenA.merge(percenA2, on='postcode')

percenA.head()
```
<b><u>Using `extractByPostcode()`</u></b>
```python
convPercenA = extractByPostcode(dataMobG, age_joined, 'priceAgreed')
# convPercenA.to_csv('../harvestApp/Model/data/convA.csv',
#                    index=False)
convPercenA.head()
```
<b><u>Interactive plot</u></b>
```python
# Creating widgets
widgetNumberA = widgets.Dropdown(options=['0 to 15', '16 to 19',
    '20 to 29', '30 to 44', '45 to 64',
    '65 to 84', '85 and over'],
    value='85 and over',
    description='Age selector')

widgetPercenA = widgets.Dropdown(options=['% 0 to 15', '% 16 to 19',
    '% 20 to 29', '% 30 to 44', '% 45 to 64',
    '% 65 to 84', '% 85 and over'],
    value='% 85 and over',
    description='Percentage',
    disabled=True)

widgetPercenConv = widgets.IntSlider(value=10, min=0,
    max=25, step=1,
    description='Filter',
    disabled=False)

# Function to link two widgets
def transform(case):
    return {'0 to 15': '% 0 to 15', '16 to 19': '% 16 to 19',
        '20 to 29': '% 20 to 29',
        '30 to 44': '% 30 to 44', '45 to 64': '% 45 to 64',
        '65 to 84': '% 65 to 84', '85 and over': '% 85 and over'}[case]
directional_link((widgetNumberA, 'value'), (widgetPercenA, 'value'), transform)

# Function to update the plot
def updatePlotA(numberColumn, percenColumn, filterA):
    print(numberColumn)
    if numberColumn == '85 and over':
        pA.title.text = 'People of ' + numberColumn
    else:
        pA.title.text = 'People between ' + numberColumn

    r1A.data_source.data['color'] = age_joined[numberColumn]
    r1A.data_source.data['percen'] = percenA[percenColumn]

    cA.high = percenA[percenColumn].max()
    cA.low = percenA[percenColumn].min()

    print(filterA)

    newData = convPercenA.loc[convPercenA['total'] > filterA]

#     r2A.data_source.data = source
    r2A.data_source.data['lat'] = newData['latitude']
    r2A.data_source.data['lon'] = newData['longitude']
    r2A.data_source.data['total'] = newData['total']
    r2A.data_source.data['total2'] = newData['total']
    r2A.data_source.data['color'] = newData['# converted']
    r2A.data_source.data['postcode'] = newData['postcode']
    r2A.data_source.data['percen'] = newData['% converted']

    push_notebook(handle=tA)

# The plots
pA =plotMap('People of 85 and over')
rA = createSource(age_joined, percenA, 'total residents',
    '85 and over', '% 85 and over', divider=2500)
cA = createColorMapper(percenA, '% 85 and over')
tA = createToolTips(rA)

r1A = pA.circle(x='lon', y='lat', size='total',
    fill_color={'field': 'percen', 'transform': cA},
    fill_alpha=0.3, source=rA)
colorBarA = ColorBar(color_mapper=cA, ticker=BasicTicker(),
    label_standoff=12, border_line_color=None, location=(0,0))
pA.add_tools(HoverTool(tooltips=tA))
pA.add_layout(colorBarA, 'right')

# -------------------------------------------------------------------------------------------------------

pAp = plotMap('Percentage converted')
rAp = createSource(convPercenA, convPercenA, 'total',
    '# converted', '% converted', divider=1)
cAp = createColorMapper(convPercenA, '% converted')
tAp = createToolTips(rAp, label3='People who showed interest',
    percenLabel='% of people who converted')

r2A = pAp.circle(x='lon', y='lat', size='total',
    fill_color={'field': 'percen', 'transform': cAp},
    fill_alpha=0.1, source=rAp)
colorBarA2 = ColorBar(color_mapper=cAp, ticker=BasicTicker(),
    label_standoff=12, border_line_color=None, location=(0,0))
pAp.add_tools(HoverTool(tooltips=tAp))
pAp.add_layout(colorBarA2, 'right')

tA = show(row(pA, pAp), notebook_handle=True)
interact(updatePlotA, numberColumn=widgetNumberA,
    percenColumn=widgetPercenA, filterA=widgetPercenConv)
```
<b><u>Calculate conversion percentage</u></b>
```python
convPercenA2 = convPercenA.drop(['latitude', 'longitude'], axis=1)
convPercenA2.head()

# Calculating conversion percentage for each qualification by postcode
newDfA = calcPercen(convPercenA2, 'total residents', '# converted',
    '% converted total')
df2 = calcPercen(convPercenA2, '0 to 15', '# converted',
    '% converted age 0 to 15')
newDfA = newDfA.merge(df2, on='postcode')

df2 = calcPercen(convPercenA2, '16 to 19', '# converted',
    '% converted age 16 to 19')
newDfA = newDfA.merge(df2, on='postcode')

df2 = calcPercen(convPercenA2, '20 to 29', '# converted',
    '% converted age 20 to 29')
newDfA = newDfA.merge(df2, on='postcode')

df2 = calcPercen(convPercenA2, '30 to 44', '# converted',
    '% converted age 30 to 44')
newDfA = newDfA.merge(df2, on='postcode')

df2 = calcPercen(convPercenA2, '45 to 64', '# converted',
    '% converted age 45 to 64')
newDfA = newDfA.merge(df2, on='postcode')

df2 = calcPercen(convPercenA2, '65 to 84', '# converted',
    '% converted age 65 to 84')
newDfA = newDfA.merge(df2, on='postcode')

df2 = calcPercen(convPercenA2, '85 and over', '# converted',
    '% converted age 85 and over')
newDfA = newDfA.merge(df2, on='postcode')

newDfA.sort_values(by='postcode')
# newDfA.to_csv('convPercenA2.csv', index=False)
# newDfA.loc[newDfA['postcode'] == 'CR0']
newDfA.head()

```
<b><u>Plot with average conversion percentage</u></b>
```python
dictA = newDfA.mean()
dictA = round(dictA, 3)

dictA = dictA.to_dict()
dictA['total'] = dictA.pop('% converted total')
del dictA['total']
dictA['0 to 15'] = dictA.pop('% converted age 0 to 15')
dictA['16 to 19'] = dictA.pop('% converted age 16 to 19')
dictA['20 to 29'] = dictA.pop('% converted age 20 to 29')
dictA['30 to 44'] = dictA.pop('% converted age 30 to 44')
dictA['45 to 64'] = dictA.pop('% converted age 45 to 64')
dictA['65 to 84'] = dictA.pop('% converted age 65 to 84')
dictA['85 and over'] = dictA.pop('% converted age 85 and over')

names = list(dictA.keys())
values = list(dictA.values())

plt.figure()
plt.title('% converted Age')
plt.plot(names,values, marker='o', markerfacecolor='red')
plt.xlabel('Age group')
plt.ylabel('Average conversion %')
for i,j in zip(names, values):
    plt.annotate(str(j), xy=(i,j), xytext=(-5,5), textcoords='offset points')
```

## General health data
<b><u>Loading and merging</u></b>
```python
# Loading health data
# Loading in the data
general_health = pd.read_excel('nomis_datasets/general_health.xlsx')

# Renaming some columns.
general_health = general_health.rename(columns={
    'postcode sector': 'postcode',
    'All categories: General health': 'general health total'})

# general_health = general_health.drop(['general health total'], axis=1)

general_health['postcode'] = general_health.postcode.str.split('\s+').str[0]

general_health = general_health.groupby(['postcode']).sum().reset_index()

general_health['postcode'] = general_health['postcode'].str.strip()
# print(general_health.loc[general_health['postcode'] == 'CR0'])
general_health.head()

# Merge with postcode data
health_joined = postcode_coords.merge(general_health,
    on='postcode', how='inner')
health_joined.head()
```
<b><u>Calculating percentage</u></b>
```python
percenH = calcPercen(dfName=health_joined,
    colAll='general health total', col1='Very good health',
    newColName='% Very good health')

percenH2 = calcPercen(health_joined, 'general health total',
    'Good health', '% Good health')
percenH = percenH.merge(percenH2, on='postcode')

percenH2 = calcPercen(health_joined, 'general health total',
    'Fair health', '% Fair health')
percenH = percenH.merge(percenH2, on='postcode')

percenH2 = calcPercen(health_joined, 'general health total',
    'Bad health', '% Bad health')
percenH = percenH.merge(percenH2, on='postcode')

percenH2 = calcPercen(health_joined, 'general health total',
    'Very bad health', '% Very bad health')
percenH = percenH.merge(percenH2, on='postcode')

# percenH['total percen'] = percenH.sum(axis=1)
healthSmall = health_joined[['postcode', 'general health total']]
percenH = healthSmall.merge(percenH, on='postcode')

percenH.head()
```
<b><u>Using `extractByPostcode()`</u></b>
```python
convPercenH = extractByPostcode(dataMobG, health_joined, 'priceAgreed')
# convPercenH.to_csv('../harvestApp/Model/data/convH.csv',
#                    index=False)
convPercenH.head()
```
<b><u>Interactive plot</u></b>
```python
# Creating the widgets
widgetNumberH = widgets.Dropdown(options=['Very good health',
    'Good health', 'Fair health', 'Bad health',
    'Very bad health'],
    value='Very bad health',
    description='Health')
widgetPercenH = widgets.Dropdown(options=['% Very good health',
    '% Good health', '% Fair health', '% Bad health',
    '% Very bad health'],
    value='% Very bad health',
    description='Percentage',
    disabled=True)
widgetPercenConvH = widgets.IntSlider(value=10, min=0, max=25,
    step=1,
    description='Filter',
    disabled=False)

# Function to link two widgets
def transformH(case):
    return {'Very good health': '% Very good health',
      'Good health': '% Good health', 'Fair health': '% Fair health',
      'Bad health': '% Bad health',
      'Very bad health': '% Very bad health'}[case]
directional_link((widgetNumberH, 'value'),
    (widgetPercenH, 'value'), transformH)

# Function to update the plot
def updatePlotH(numberColumn, percenColumn, filterH):
    print(numberColumn)
    pH.title.text = numberColumn
    r1H.data_source.data['color'] = health_joined[numberColumn]
    r1H.data_source.data['percen'] = percenH[percenColumn]

    cH.high = percenH[percenColumn].max()
    cH.low = percenH[percenColumn].min()    

    print(filterH)
    newData = convPercenH.loc[convPercenH['total'] > filterH]

#     r2H.data_source = ColumnDataSource(newData)
    r2H.data_source.data['lat'] = newData['latitude']
    r2H.data_source.data['lon'] = newData['longitude']
    r2H.data_source.data['total'] = newData['total']
    r2H.data_source.data['total2'] = newData['total']
    r2H.data_source.data['color'] = newData['# converted']
    r2H.data_source.data['postcode'] = newData['postcode']
    r2H.data_source.data['percen'] = newData['% converted']

    push_notebook(handle=tH)

# The plots
pH = plotMap('People with very bad health')
rH = createSource(health_joined, percenH, 'general health total',
    'Very bad health', '% Very bad health', divider=3000)
cH = createColorMapper(percenH, '% Very bad health')
tH = createToolTips(rH)

r1H = pH.circle(x='lon', y='lat', size='total',
    fill_color={'field': 'percen', 'transform': cH},
    fill_alpha=0.3, source=rH)
colorBar = ColorBar(color_mapper=cH, ticker=BasicTicker(),
    label_standoff=12, border_line_color=None, location=(0,0))
pH.add_tools(HoverTool(tooltips=tH))
pH.add_layout(colorBar, 'right')

# -------------------------------------------------------------------------------------------

pHp = plotMap('Percentage converted')
rHp = createSource(convPercenH, convPercenH, 'total',
    '# converted', '% converted', divider=1)
cHp = createColorMapper(convPercenH, '% converted')
tHp = createToolTips(rHp)

r2H = pHp.circle(x='lon', y='lat', size='total',
    fill_color={'field': 'percen', 'transform': cHp},
    fill_alpha=0.3, source=rHp)
colorBarH2 = ColorBar(color_mapper=cHp, ticker=BasicTicker(),
    label_standoff=12, border_line_color=None, location=(0,0))
pHp.add_tools(HoverTool(tooltips=tHp))
pHp.add_layout(colorBarH2, 'right')

tH = show(row(pH, pHp), notebook_handle=True)
interact(updatePlotH, numberColumn=widgetNumberH,
    percenColumn=widgetPercenH, filterH=widgetPercenConvH)
```
<b><u>Calculate conversion percentage</u></b>
```python
convPercenH2 = convPercenH.drop(['latitude', 'longitude'], axis=1)
convPercenH2.head()

# Calculating conversion percentage for each housing type by postcode
newDfHC = calcPercen(convPercenH2, 'general health total',
    '# converted', '% total converted')
df2 = calcPercen(convPercenH2, 'Very good health',
    '# converted', '% converted Very good health')
newDfHC = newDfHC.merge(df2, on='postcode')

df2 = calcPercen(convPercenH2, 'Good health',
    '# converted', '% converted Good health')
newDfHC = newDfHC.merge(df2, on='postcode')

df2 = calcPercen(convPercenH2, 'Fair health',
    '# converted', '% converted Fair health')
newDfHC = newDfHC.merge(df2, on='postcode')

df2 = calcPercen(convPercenH2, 'Bad health',
    '# converted', '% converted Bad health')
newDfHC = newDfHC.merge(df2, on='postcode')

df2 = calcPercen(convPercenH2, 'Very bad health',
    '# converted', '% converted Very bad health')
newDfHC = newDfHC.merge(df2, on='postcode')

# newDfHC.to_csv('convPercenH2.csv', index=False)
newDfHC.head()
```
<b><u>Plot with average conversion percentage</u></b>
```python
dictH = newDfHC.mean()
dictH = round(dictH, 3)
dictH = dictH.to_dict()

dictH['total'] = dictH.pop('% total converted')
del dictH['total']
dictH['very good'] = dictH.pop('% converted Very good health')
dictH['Good'] = dictH.pop('% converted Good health')
dictH['Fair'] = dictH.pop('% converted Fair health')
dictH['Bad'] = dictH.pop('% converted Bad health')
dictH['Very bad'] = dictH.pop('% converted Very bad health')

names = list(dictH.keys())
values = list(dictH.values())

plt.figure()
plt.title('% converted Health')
plt.plot(names, values, marker='o', markerfacecolor='red')
plt.xlabel('Health group')
plt.ylabel('Average conversion %')
for i,j in zip(names, values):
    plt.annotate(str(j), xy=(i,j), xytext=(-5,5),
      textcoords='offset points')
```
<b><u>Running `extractByPostcode()` again and plotting scatter plots</u></b>
```python
test = extractByPostcode(dataMobG, percenH, 'priceAgreed')
test.head()

g = sns.PairGrid(test, y_vars=['% converted'],
    x_vars=['% Very good health', '% Good health'], height=5)
g.map(sns.regplot)

g1 = sns.PairGrid(test, y_vars=['% converted'],
    x_vars=['% Fair health', '% Bad health', '% Very bad health'], height=7)
g1.map(sns.regplot)
```
