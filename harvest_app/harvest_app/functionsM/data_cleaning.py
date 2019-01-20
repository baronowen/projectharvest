import numpy as np
import pandas as pd
import os

def dropColumns(dfName, justDrop, columnList):
    """
    Function to drop columns in one of two ways:
        Dropping specified columns.
        Dropping where ALL specified columns have NaN values.
    Keep in mind that all variables in columnList HAVE to be a string.
    Parameters
    ----------
    justDrop : boolean
        Boolean used to determine how to drop.
        True just drops the columns.
        False drops where ALL columns have NaN values.
    """
    if columnList:
        temp = dfName.loc[:]
        # Check wether justDrop is a boolean.
        if isinstance(justDrop, bool):
            if justDrop == True:
                # Drop columns if True.
                temp = dfName.drop(columnList, axis=1)
            elif justDrop == False:
                # Drop empty columns only when False.
                temp = dfName.dropna(subset=columnList, how='all')
            else:
                return 'Need a boolean.'
            return temp
        else:
            return 'Function needs a boolean!'
    else:
        return 'No columns selected!'

def copyAndDrop(dfName, copyList, dropList, fileName):
    """
    A function to make a backup of certain columns and
        drop them from the original. Files will be stored in the temp folder.
    Keep in mind that copyList and dropList both HAVE to be a list
        and HAVE to contain strings.
        Files will be stored as CSV in the temp folder.
    """
    if copyList:
        if dropList:
            if fileName != "":
                # Copy the columns.
                copy = dfName[copyList]
                # Drop column in dropList.
                dfName.drop(dropList, axis=1, inplace=True)
                # Save copied dataframe.
                copy.to_csv('data/temp/' + fileName + '.csv', index=False)
                return dfName
            else:
                return 'Give a name for the copy!'
        else:
            return 'No columns selected to drop!'
    else:
        return 'No columns selected to copy!'

def fillEmptyColumns(dfName, fillWith, columnList):
    """
    Fills specified columns with the value specified in fillWith.
    Keep in mind that all variables in columnList HAVE to be a string.
    """
    if columnList:
        if fillWith != "":
            # Loop over columns in list to fill it.
            for col in columnList:
                dfName[col].fillna(fillWith, inplace=True)
            return dfName
        else:
            return 'Fill in a value to fill the column with!'
    else:
        return 'Select empty columns to fill!'

def stringify(dfName, columnList):
    """
    A function that converts certain columns to string type.
    """
    if columnList:
        for c in columnList:
            dfName[c] = dfName[c].astype(str)
        return dfName
    else:
        return 'Select columns to stringify!'

def rename(dfName, column, newName):
    """
    A function that is used to rename a column.
    Keep in mind that this function can only rename 1 column at a time.
    """
    if column != "":
        if newName != "":
            dfName = dfName.rename(columns={column: newName})
            return dfName
        else:
            return 'Fill in a new column name!'
    else:
        return 'Select a column to rename!'

def removeW(dfName, columnList):
    """
    This function removes potential whitespaces from a string.
    Can only be used on columns with strings.
    """
    if columnList:
        for col in columnList:
            if dfName[col].dtype == object:
                dfName[col] = dfName[col].str.strip()
            else:
                return 'Selected column(s) have to be a string!'
        return dfName
    else:
        return 'Select one or more columns to remove whitespaces from!'

def shortenPostcode(dfName, column):
    """
    This function is meant to strip away the last digit(s) of postcodes.
    Keep in mind that once stripped, it WILL perform a group by operation.
    """
    if column != "":
        # Remove characters after space.
        dfName[column] = dfName[column].str.split('\s+').str[0]
        dfName = dfName.groupby([column]).sum().reset_index()
        return dfName
    else:
        return 'Select the column with postcodes to shorten it!'
