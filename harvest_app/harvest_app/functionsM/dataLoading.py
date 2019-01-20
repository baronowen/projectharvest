from tkinter import messagebox
import pandas as pd

def loadData(fileName, fileType):
    """
    Load in data.
    Function only supports excel and csv files.
    Parameters
    ----------
    fileName : string
        A string specifying the name or path to a file.
    fileType : string
        A string needed to let the function know what it is reading.
    Returns
    -------
    temp : pd.DataFrame
        A dataframe containing the data.
    """
    try:
        if (fileType == 'xlsx' or fileType == 'xls' or fileType == 'excel'):
            temp = pd.read_excel(fileName)
        elif fileType == 'csv':
            temp = pd.read_csv(fileName)
        else:
            return
    except FileNotFoundError:
        return 'FileNotFoundError'
    else:
        return temp
