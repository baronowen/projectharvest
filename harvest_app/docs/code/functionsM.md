# Package functionsM
This package contains modules with functions. These modules are:
* apiFunctions
* clustering
* data_cleaning
* dataLoading
* dataManipFunctions
* extraFunctions
* guiFunctions

Every module will be explained in their own sections. These sections will contain the function explanation of all functions inside that module.

## ApiFunctions
This module contains the functions that call the delegators in the package 'api_calls'. Think of this module as a bridge between the delegators and the GUI. All the functions in this module only pass on parameters to the delegators, which in turn pass it on to the functions that call the API.
The functions in this module are:
* createClient
Function that loads in the credentials from the `googleads.yaml` file in `data/config file API/`.
* loadAccounts
* loadCampaigns
* load1Campaign
* loadCampaignCriteria
* loadCampaignCriteriaWithBid
* addCampaignCriteria
* removeCampaignCriteria
* UpdateCampaignCriteria
* callCampCritApi

<hr/>

## Clustering
The functions that belong in this module are functions that cluster data into categories/clusters/bins. At the moment of writing this module only has one function, namely 'clusterManual()'. If there is a need for more functions that can cluster data in the future, this is the place to keep those functions.

<b><u>ClusterManual</u></b>
This function clusters the data using pandas `.cut()` function. This creates an <i>n</i> amount of clusters with equal interval size. However, this function first checks whether labels have been specified and whether the number of labels is equal to the number of bins. Only when both are true, will this function use `.cut()`.

Parameters:
* dfName
DataFrame type, the name of the dataframe with the column that is to be clustered.
* toCluster
String type, the name of the column that is to be clustered.
* nBins
Integer type, the number of bins (or clusters/categories) that is to be made.
* labelList
List of Strings, The names of the labels for the clusters. Go from worse to best.

<hr/>

## Data_cleaning
This module contains functions for the cleaning of data. Functions within are:
* dropColumns()
* copyAndDrop()
* fillEmptyColumns()
* stringify()
* rename()
* removeW()
* shortenPostcode()

All these functions have one parameter in common, namely the parameter `dfName`. This parameter specifies the name of the dataframe that is to be used.

If there is a need for extra cleaning functions in the future, this is the place to keep those functions.

<b><u>DropColumns</u></b>
This function has two ways of dropping, which is determined by a `Boolean`. The first way is dropping all columns in a list, and the second way is dropping the rows where all columns in a list are either empty or have NaN values inside.

Parameters:
* justDrop
Boolean type, determines which of the two drop options to use. True means just dropping, false means dropping rows where all columns are empty (or NaN).
* columnList
List of strings, the names of the columns that are to be dropped. Names have to be inside the dataframe specified in dfName.

<b><u>CopyAndDrop</u></b>
This function is used to create a backup of certain columns and removing them from the original. This is done by specifying columns to copy and drop. The columns that are to be copied are stored in a CSV file with the specified name, and the column that are to be dropped are dropped from the original.

Parameters:
* copyList
List of strings, the names of the columns that are to be copied.
* dropList
List of strings, the names of the columns that are to be dropped.
* fileName
String, the name of the file in which the copy will be stored.

<b><u>FillEmptyColumns</u></b>
A function to fill a specified column with the specified value. This function is used to get rid off columns that have NaN values within them. It does this by looping over the columns specified, and calling pandas `.fillna()` function on these columns.

Parameters:
* fillWith
String type, the value with which the empty columns will be filled.
* columnList
List of strings, the name of the column(s) that is/are to be filled.

<b><u>Stringify</u></b>
A small function that uses pandas `.astype()` function to change the datatype of a column to a string type.

Parameter:
* columnList
List of strings, the names of the column(s) that is/are to be stringified.

<b><u>Rename</u></b>
A function that renames a column name to the new specified name. It does this by using pandas `.rename()` function.

Parameters:
* column
String type, the name of the column that is to be renamed.
* newName
String type, the new name of the column.

<b><u>RemoveW</u></b>
This function removes the whitespaces from a column in a dataframe. it does this by looping over all columns specified in a list and stripping the whitespaces away. The columns have to be of string type, or this function won't work.

Paremeter:
* columnList
List of strings, the names of the columns.

<b><u>ShortenPostcode</u></b>
This function is used to shorten a British postcode to the first part of a postcode. For example, 'EC2A 4DX' becomes 'EC2A'. This is done by splitting the postcode string on the space and selecting only the first part. When the splitting is done, the function does a group by on the same column, takes the sum and resets the index.

Parameter:
* column
String type, the name of the column with postcodes in it.

<hr/>

## DataLoading
This module holds the function that loads the data into a dataframe. This function is `loadData()`. The way it works is it first checks whether file type is excel or CSV and then calls either pandas `.read_excel()` or `.read_csv()` function.
If there is a need for other data loading functions in the future, this is the place to keep those functions.

<b><u>LoadData</u></b>
Parameters:
* fileName
String type, the name of the file. Has to include either `.xlsx` or `.csv`.
* fileType
String type, represents the type of file loaded in. Has to be either `xlsx`/`xls`/`excel` or `csv`.

<hr/>

## DataManipFunctions
This module contains functions that manipulate the data. The functions in this module are:
* encodeColumn()
* extractConv()
* calcPercen()
* saveData()
* mergeDataframes()

The functions `encodeColumn`, `calcPercen` and `saveData` all have one parameter in common, namely `dfName`. This parameter represents the dataframe that is to be used in that function and is of the DataFrame type.


<b><u>EncodeColumn</u></b>
This is a small function that 'label encodes' a column. This means that a column like postcode or a category becomes a numerical representation of that postcode or category.
This function does this by first creating a `LabelEncoder` instance (`LabelEncoder` is imported from `sklearn.preprocessing`).
With the `LabelEncoder` created the function uses the `.fit()` method on the column that is to be label encoded. Once fitted, the function uses the `.transform()` method to transform the column to the new numerical representation.

Parameters:
* toEncode
String type, the name of the column that is to be encoded. The column that is to be encoded has to be of the String type.
* newCol
String type, the name of the new column.

<b><u>ExtractConv</u></b>
This function extracts the number of people who showed interest and the number of people who converted (bought something) from a dataframe. Once these two have been extracted, the difference and conversion percentage is calculated.

Before calling this function the data that is used has to be cleaned! The main cleaning function that has to be used is `dropColumns()` with the `justDrop` parameter set to `False`. Other cleaning functions are recommended.

The function first uses the `.value_counts()` function to count all the occurrences of the specified postcode column. This indicates the total number of people who showed interest. These values are returned as a pandas Series object, so it is converted to a DataFrame object.
The next step for the function is extracting all rows where the conversion column specified is higher than zero, and again using the `.value_counts()` function to count all the occurrences of the specified postcode column. This indicates the number of people who converted. These values are also converted to a DataFrame object.

The third step is to merge these two dataframes together on the specified postcode column, using a 'outer' merge.
The final step for the function is to fill the empty columns with value 0, and calculating the difference and conversion percentage.

Parameters:
* convData
DataFrame type, the name of the dataframe containing the (cleaned) conversion data.
* convCol
String type, the name of the column indicating whether a conversion took place.
* postcodeCol
String type, the name of the column containing the postcodes.

<b><u>CalcPercen</u></b>
This function calculates the conversion percentages for the columns specified in a list. It does this by first checking whether certain columns are present in the dataframe. Once this is checked, it loops over the columns in the list and creates a temporary dataframe. It then starts another loop (inside the previous one) that uses pandas `.itertuples()` to loop over every row in this temporary dataframe and calculate the percentage for that row.

Mandatory parameter:
* colAllList
List of strings, contains the names of the columns that a percentage is to be calculated of.

Optional parameter:
* col1
String, represents the name of the column containing the number of people who converted (has a default value and is thus optional).

<b><u>SaveData</u></b>
A small function that writes the dataframe to a CSV file. This file is stored in the data folder.

Parameter:
* fileName
String type, the name of the new file.

<b><u>MergeDataframes</u></b>
A function that performs an inner join on two dataframes. Supports two ways of joining, either with the same column in both dataframes, or by specifying `leftOn` and `rightOn`. Both options lead to a merge, the only difference being the parameters.

Mandatory parameters:
* df1
DataFrame type, dataframe number 1, will be on the left during the merge.
* df2
DataFrame type, dataframe number 2, will be on the right during the merge.
* mergeOn
String type, the name of the column that is to be merged upon. Only required when `leftOn` and  `rightOn` have not been specified.

Optional parameters:
* how
String type, the type of join that is to be performed. Defaults to 'inner'.
* leftOn
String type, the name of the column in the left dataframe that is to be used for merging. Defaults to None and is not required when `mergeOn` is specified.
* rightOn
String type, the name of the column in the right dataframe that is to be used for merging. Defaults to None and is not required when `mergeOn` is specified.

<hr/>

## ExtraFunctions
This module contains functions that don't belong in other modules. If this module grows it might happen that functions inside which belong together are moved to their own module.
The functions inside are:
* updateClientId
* retrieveFromConfig
* retrieveClientId
* assignBidMod

<b><u>UpdateClientId</u></b>
This function updates 'client customer id' in the `googleads.yaml` file, which is located in `data/config file API/`. This is the only part of this file that is updated using this function.

Mandatory parameters:
* clientId
String type, the ID that is to be used in the `googleads.yaml` file.

Optional parameters:
* fileName
String type, the path to the `googleads.yaml` file. Defaults to this file in `data/config file API`.
* rowNumber
Integer type, the row number that contains the 'client customer id'. Defaults to this row in the `googleads.yaml` file.

<b><u>RetrieveFromConfig</u></b>
This function retrieves all information from the file called `config.txt` in `data/config file API/` and puts it in a dictionary which is returned. This happens by reading all lines, looping over these lines, stripping the line into two parts and adding the second part to a dict with an identifier. The first part identifies what the second part means, for example, `client_ID_to_use: 7548889362`.

Optional parameter:
* filename
String type, the path to the `config.txt` file, defaults to `data/config file API/config.txt`.

<b><u>RetrieveClientId</u></b>
This function retrieves the current client ID from the `googleads.yaml` file. It does this by opening the file, looping over all lines and retrieving the line where the row number is the number specified.
This line then gets split using this line:
```python
string = string.split(': ')[1]
```

After splitting, the string is stripped to remove any remaining whitespaces. The final step is starting another loop to remove the quotes surrounding the ID.

Optional parameters:
* fileName
String type, the path to the `googleads.yaml` file. Defaults to this file in the home directory.
* rowNumber
Integer type, the row number that contains the 'client customer id'. Defaults to this row in the `googleads.yaml` file.

<b><u>AssignBidMod</u></b>
This function assigns a bid modifier percentage to categories. This is done by counting the number of times a unique value inside a column occurs. The result is then converted to a dict, which length becomes the number of bins required.
After getting the length, a list is made of the keys in the previous dictionary. This list will be used later. The next step is filling a list with the percentage range, specified by `lowPercen` and `highPercen`, using a loop. The max size of a bin can then be calculated with the length of this range list and the number of bins.
With these two present, a while loop is started that continues as long as an iterator is smaller than the number of bins. Inside the loop the range list is split into sub lists and these sub lists are added to another list.
After the while loop ended, a normal loop is started that loops over this list of sub lists. Inside this loop the mean is calculated for each sub list and the result is appended to a different list.
The last step is to combine the category list and the list with the averages together into a dictionary. this is done by the following line of code:
```python
dict(zip(catList, percenList))
```

<hr/>

## GuiFunctions
This module contains all the functions that are related to the GUI. Some functions inside also act as a 'bridge' between the GUI and other modules inside this package. The functions inside are:
* validateDataLoading()
* loadingData()
* refreshLists()
* retrieveItems()
* saveDataframe()
* showData()
* showHideFrames()
* disableWidget()
* isInt()
* emptyWidgets()

<b><u>ValidateDataLoading</u></b>
This function checks the input before loading in a dataset. It checks whether file path has been filled in, and if filetype and file extension match (xlsx with xlsx and csv with csv). If the conditions are met, it returns the file path and file type back to the caller.

Parameters:
* pathEntry
String type, is the path to the file that is to be loaded in. Can be absolute or relative.
* typeVar
String type, is the file type that is to be loaded and has to correspond with the file extension which can be deduced from pathEntry.

<b><u>LoadingData</u></b>
This function calls `loadData()`, which returns the data in a dataframe format. After loading it checks wheter a string is returned, because a string indicates an error. If the data is successfully returned, it shows a preview and or refreshes list boxes. This differs per page.

Mandatory parameters:
* pathEntry
String type, same as with `validateDataLoading`()
* typeVar
String type, same as with `validateDataLoading()`
* page
String type, represents the page from which this function is called. Behaviour differs for every page.

Optional parameters (Necessary when it is wished to update the GUI):
* listboxes
List of tkinter Listboxes, the names of the list boxes that are to be updated.
* previewLabel
Tkinter Label, name of the previewLabel to show a review of the data.
* shapeLabel
Tkinter Label, name of the shapeLabel to show the shape of the data.
* saveButton
Tkinter Button, name of the button that is used for saving data to another CSV.
* bool
Boolean type, used to determine in which dataframe to store the loaded data. Only used in the merging page.

<b><u>RefreshLists</u></b>
This function refreshes the listboxes specified in the list. It does this by first retrieving the columns from the dataframe specified. It then loop over all the list boxes and empties them. While still inside this loop it starts a loop over the column list and adds the columns to the list boxes.

Parameters:
* dfName
Dataframe type, the name of the dataframe that is to be used.
* listBoxList
List of list boxes, the names of the list boxes that are to be updated.

<b><u>RetrieveItems</u></b>
This function retrieves information from either a list box or a text box.

Parameters:
* container
Tkinter object, the name from which information is to be retrieved.
* retrieveFrom
String type, determines from what to retrieve. So far only supports `'listBox'` and `'textBox'`.

<b><u>SaveDataFrame</u></b>
This function checks whether data can be saved (name has to be filled in and there has to be a dataframe with data inside), and if it can be saved, calls the `saveData()` function in the module `dataManipFunctions`. After saving the data, the function `emptyWidgets` is called (within this module).

Parameters:
* saveName
String type, the name of the new file.
* dfName
DataFrame type, the dataframe that is to be saved.
* saveButton
Tkinter Button, the name of the button that is pressed to save the data.
* widgetDictList
Dictionary type, a dictionary of widgets that are to be emptied.

<b><u>ShowData</u></b>
A function used to show a preview of the data. This function enables the save button aswell by default, but this can be turned of by passing `True` to the `justLook` parameter.

Mandatory parameters:
* dfName
DataFrame type, the name of the dataframe with the data that is to be shown.
* previewLabel
Tkinter Label, the name of the label that will hold the preview of the data.
* shapeLabel
Tkinter Label, the name of the label that will hold the shape of the data.

Optional parameters
* buttonToChange
Tkinter Button, the name of the button that is pressed to save the data.
* justLook
Boolean type, determines whether or not the button needs to be updated. If true, `buttonToChange` has to be specified.

<b><u>ShowHideFrames</u></b>
This function hides frames that are no longer needed, and shows those that are. Both parameters have a default value, which makes them optional in the eyes of Python, but one of them or both has to be specified if anything is to change. Uses the function `.grid_remove()` to 'hide' frames and `.grid()` to show them.

Parameters:
* hideList
List of frames, a list of tkinter frames that is to be hidden.
* showList
List of frames, a list of tkinter frames that is to be shown.

<b><u>DisableWidget</u></b>
This function is used to disable buton widgets. This is done by changing the state parameter in the `.configure()` function. This function can only be used on Tkinter Widgets.

Parameters:
* name
Tkinter Widget type, the name of the widget that is to be disabled.
* type
String type, the type of widget that is to be disabled. Only supports 'button'.

This function can be expanded to support other types beside buttons.

<b><u>IsInt</u></b>
A small function that checks whether the input is an integer.

<b><u>EmptyWidgets</u></b>
This function empties the widgets specified. It does this by looping over the list of dictionaries and checking what type is specified. This function supports entry fields, list boxes, text boxes and labels, and can be expanded to support other types in the future.

Parameters:
* listOfDicts
List of dictionaries, dictionary has to contain the widget name and type. If type is an entry, special also has to be present. Type is a String, special is a Boolean.

The optional parameters key1, key2 and key3 are the names of the keys in the dictionary. These all have a default value.
