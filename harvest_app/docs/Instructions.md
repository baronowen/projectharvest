# Instruction manual

<b><u>AdWords page</u></b>
The AdWords page is used to interact with the Google AdWords API. This is done through the right part of the GUI, and can be used to retrieve accounts, campaigns and information about one specific campaign. Once a campaign is selected, more information regarding that campaign is shown. This includes things like the start and end date, aswell as locations where that campaign is being targeted. In this part it is also possible to add locations to target, remove locations and update the bid modifier percentage for that location. See image below.
1. Adding is done by typing a postcode into the text field with label 'New postcode' (below button for removing, above button for adding).
2. Removing is done by selecting one or more postcodes from the list box and pressing the remove button.
3. Updating is done by selecting one or more postcodes, typing a new bid modifier precentage in the text field for new bid modifier and pressing the update button.

<img src='images/adwords1.png' width=50% title='adwords page' alt='adwords page'/>

The left part of the GUI is used to load in a dataset. This dataset is meant to contain clustered or categorized data. This data is used when pressing the button 'Auto target best categories', and pressing this button will not work without having this data loaded in.
This button, 'Auto target best categories', first assigns a percentage to each category and then targets the postcodes with the best categories with that percentage as their bid modifier percentage. If one or more postcodes are already being targeted, it updates their bid modifier percentage.

These percentages are assigned based on a minimum and maximum percentage, and these two can be adjusted by changing the value behind `min_percen` and `max_percen` respectively. By changing these percentages the final percentages for each category will be smaller (when decreasing the min and max) or bigger (when increasing the min and max).
For more information on how these percentages are assigned, see the code appendix called functionsM in `docs/code/`.

In this config file it is also possible to change the ID of the client account that is to be used by the application. Do this by changing the value behind `client_ID_to_use`.

All three of these values can be changed while the application is running.

<b><u>Cluster page</u></b>
The cluster page is used to cluster data using the maual cluster method. This method uses pandas `.cut()` function.
The left part of the GUI is where the data is loaded in. After loading the data, a preview of it is shown below the dropdown in the right part. See the screenshot below.

<img src='images/cluster 3.png' width=40% title='cluster page 1' alt='cluster page 1'/>

The clustering is done by selecting a column to cluster on from the list box, typing the number of clusters that are wanted, typing the labels for each category and pressing the button 'Cluster manually'. The labels go in the order bad to best, and the number of labels has to match the number of clusters, pressing the button will not work otherwise.
Pressing the cluster button ads two extra columns to the dataframe. These columns contain the cluster/category label, and the numeric representation of that label.

<b><u>Data loading and cleaning page</u></b>
This page is used to clean the data that is loaded in. The cleaning supports the following operations:
* Dropping columns
* Dropping empty columns only
* Copying and dropping
* Filling empty columns
* Stringifying a column
* Renaming a columns name
* Removing of whitespaces
* Shorten postcode.


For most of these functions it is a matter of selecting one or more columns, and pressing the button. A few functions, copying and dropping, filling empty columns and renaming require a little more.
<img src='images/copy and drop.png' width=40% title='copy and drop' alt='copy and drop'/> <img src='images/filling.png' width=23% title='filling empty columns' alt='filling empty columns'/> <img src='images/renaming.png' width=30% title='renaming' alt='renaming'/>
Copying and dropping requires the user to select columns that are to be copied, select the ones that are to be dropped, type the name for the file containing the copied columns and pressing the button. See the first screenshot above.

Filling empty columns requires the user to selecct the columns that are empty and are to be filled, type the value those columns are to be filled with and pressing the button. See the middle screenshot above.

Renaming only requires the user to select one column and type the new name of that column. See the last screenshot above.

<b><u>Data manipulation page</u></b>
The data manipulation page is used to perform operations that don't belong in the cleaning page. Supported operations are:
* Extracting potential conversions
* Encoding a column
* Calculating percentages

All these function only require the user to select one or more columns and to press the button.
For more information regarding how these functions work, please refer to the data manipulation part of the `functionsM.md/pdf` file.

<b><u>Data merging page</u></b>
This page is used to merge two datasets together. This is done by loading two datasets (Left part of screenshot below), selecting one column from both listboxes and pressing the button.

<img src='images/merging 1.png' width=50% title='merging' alt='merging'/>
<hr>
For more information regarding the inner workings of the functions, see the documentation files.

* The files `api_calls.md` and `api_functions.md` contain the documentation for the modules inside the packages with the same name.
* The file `functionsM.md` contains the documentation for the modules inside the package with the same name.
* The file `pages.md` contains a reference to the functions in the modules inside the package with the same name.
