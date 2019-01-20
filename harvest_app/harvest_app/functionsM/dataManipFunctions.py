import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import LabelEncoder

def encodeColumn(dfName, toEncode, newCol):
    """
    A function that encodes a column.
    """
    try:
        # Creating a LabelEncoder instance.
        labelEncoder = LabelEncoder()
        if isinstance(toEncode, str) and isinstance(newCol, str):
            # Encoding the column.
            labelEncoder.fit(dfName[toEncode])
            dfName[newCol] = labelEncoder.transform(dfName[toEncode])
            return dfName
        else:
            return
    except TypeError as te:
        print(te)

def extractConv(convData, convCol, postcodeCol):
    """
    This function extracts the number of people who showed interest
    and the number of people who already converted. Once this is extracted,
    it calculates the difference and the percentage of people who converted.
    """
    try:
        if isinstance(convCol, str) and isinstance(postcodeCol, str):
            # Getting value_counts of postcodes.
            total = convData[postcodeCol].value_counts()
            # Creating a dataframe of total.
            total = total.to_frame().reset_index()
            # Renaming columns.
            total = total.rename(columns={'index': postcodeCol,
                postcodeCol: 'total'})
            # Extracting postcodeCol and convCol.
            converted = convData[[postcodeCol, convCol]]
            # Extracting rows where convCol is higher than 0.
            converted = converted.loc[converted[convCol] > 0]
            # Getting value_counts.
            converted = converted[postcodeCol].value_counts()
            # Creating dataframe of converted.
            converted = converted.to_frame().reset_index()
            # Renaming columns.
            converted = converted.rename(columns={'index': postcodeCol,
                postcodeCol: '# converted'})
            # Merging total with converted.
            combo = total.merge(converted, on=postcodeCol, how='outer')
            # Filling the empty columns.
            combo.fillna(0, inplace=True)
            # Calculating difference and percentage converted.
            combo['difference'] = (combo['total'] - combo['# converted'])
            combo['% converted'] = ((combo['# converted'] / combo['total']) * 100)
            return combo
        else:
            return 'Type error'
    except TypeError:
        return 'Column selected contains strings and not integers!'
    except ValueError:
        return 'Can not do this on postcode!'

def calcPercen(dfName, colAllList, col1='# converted'):
    """
    Calculates the conversion percentage.
    Keep in mind that all columns passed to this function
    have to contain a space!
    """
    tempDict = {}
    noSpace = []
    if 'postcode' in dfName.columns:
        temp2 = dfName[['postcode']]
        if colAllList:
            # Checking wether col1 exists in dataframe.
            if col1 in dfName.columns:
                for col in colAllList:
                    if not (' ' in col):
                        noSpace.append(col)
                    else:
                        temp = dfName[['postcode', col1, col]]
                        # Looping over dataframe using itertuples
                        for row in temp.itertuples():
                            # Getting the attributes needed.
                            postcode = getattr(row, 'postcode')
                            x = getattr(row, '_2')
                            y = getattr(row, '_3')
                            # Checking wether one of them is 0.
                            if x == 0 or y == 0:
                                z = 0
                            else:
                                # Calculating percentage.
                                z = (x/y) * 100
                            # Creating dictionary.
                            tempDict[postcode] = z
                        # Converting dictionary to dataframe.
                        temp2['% ' + col] = temp2['postcode'].map(tempDict)
                if noSpace:
                    return 'No space in column(s) "%s".' % noSpace
                else:
                    return temp2
            else:
                return "No column called '%s'" % col1
        else:
            return 'Select a column from the list box!'
    else:
        return "No column called 'postcode'!"

def saveData(dfName, fileName):
    """
    A function to save a dataframe to a csv file
    """
    if fileName != "":
        dfName.to_csv('data/' + fileName + '.csv', index=False)
    else:
        pass
        
def mergeDataframes(df1, df2, mergeOn=None, how='inner', leftOn=None, rightOn=None):
    """
    A function that performs a merge operation on two dataframes.
    """
    if mergeOn is not None and (leftOn is None and rightOn is None):
        temp = df1.merge(df2, on=mergeOn, how=how)
    elif (leftOn is not None and rightOn is not None) and mergeOn is None:
        temp = df1.merge(df2, left_on=leftOn, right_on=rightOn, how=how)
    else:
        return 'Specify columns to merge on!'
    return temp
