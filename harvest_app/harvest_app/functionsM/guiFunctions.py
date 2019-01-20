from tkinter import messagebox

from .dataLoading import *
from .dataManipFunctions import *

def validateDataLoading(pathEntry, typeVar):
    """
    A function that validates wether data can be loaded in.

    Does not check wether a file exists, only checks input fields.
    """
    # Retrieve text in entry fields.
    filePath = pathEntry.get()
    fileType = typeVar.get()
    # Check wether entry field is empty.
    if filePath == "":
        messagebox.showerror(message="File path is empty,\n"
            "please fill in a path.")
        return None
    else:
        # Get file extension (last 4 or 5 charachters(including '.')).
        ext1 = filePath[-4:]
        ext2 = filePath[-5:]
        # Check wether one of the extensions matches.
        if ext1 == fileType or ext2 == fileType:
            # messagebox.showinfo(message='File type and file extension match.')
            fileType = fileType.replace('.', '')
            return filePath, fileType
        else:
            filePath = None
            fileType = None
            messagebox.showerror(message="File type and extension do not match!"
                "\nMake sure file extension corresponds with file type!")
            return filePath, fileType

def loadingData(pathEntry, typeVar, page, listboxes=None, previewLabel=None, shapeLabel=None, saveButton=None, bool=True):
    """
    This function calls the loadData function, shows the data in preview labels
    and refreshes the listboxes passed to it.
    Parameters:
    -----------
    page: str
        A string indicating which page.
        Updates specific widgets dependent on the page.
    listboxes: list
        A list of listboxes that you want to refresh
    bool: Boolean
        A boolean indicating which dataframe is used for merging.
    """
    try:
        # Call validateDataLoading.
        filePath, fileType = validateDataLoading(pathEntry, typeVar)
        # Check wether input fields are not None after validating.
        if filePath is not None and fileType is not None:
            # Load data and check if it is a string
            temp = loadData(filePath, fileType)
            if isinstance(temp, str):
                if temp == 'FileNotFoundError':
                    messagebox.showerror(message='File does not exist.')
                    return
                else:
                    messagebox.showerror(message='error: %s' % temp)
                    return
            else:
                pass
            # Check which page.
            if page == 'dataLC':
                showData(temp, previewLabel,
                    shapeLabel, buttonToChange=saveButton)
                refreshLists(temp, listboxes)
                return temp
            elif page == 'merging':
                if bool:
                    refreshLists(temp, listboxes)
                    return temp
                elif not bool:
                    refreshLists(temp, listboxes)
                    return temp
                else:
                    return None
            elif page == 'dataManip':
                showData(temp, previewLabel,
                    shapeLabel, buttonToChange=saveButton)
                refreshLists(temp, listboxes)
                return temp
            elif page == 'clustering':
                showData(temp, previewLabel, shapeLabel, buttonToChange=saveButton)
                refreshLists(temp, listboxes)
                return temp
            elif page == 'adwords':
                showData(temp, previewLabel, shapeLabel, justLook=True)
                return temp
            else:
                return None
        else:
            return None
    except TypeError as te:
        print(te)
    except AttributeError as ae:
        print(ae)

def refreshLists(dfName, listBoxList):
    """
    This function makes sure that the listboxes specified
    show the correct columns.
    """
    # Get a list of columns of the dataframe.
    colList = list(dfName.columns.values)
    # Loop over the list boxes to update them.
    for listBox in listBoxList:
        # Empty the list box.
        listBox.delete(0, 'end')
        i = 0
        # Loop over the columns
        for col in colList:
            i += 1
            # Add a column
            listBox.insert(i, col)

def retrieveItems(container, retrieveFrom):
    """
    A function that can retrieve the selected items from a listbox
    or the typed values from a text box.
    The parameter retrieveFrom determines from where it is retrieved.
    """
    if retrieveFrom == 'listBox':
        items = container.curselection()
        values = []
        for i in items:
            value = container.get(i)
            values.append(value)
        return values
    elif retrieveFrom == 'textBox':
        temp = container.get('1.0', 'end-1c')
        line = temp.split(',')
        lineList = []
        for i in line:
            i = i.strip()
            lineList.append(i)
        return lineList
    else:
        return

def saveDataframe(saveName, dfName, saveButton, widgetDictList):
    """
    The function that calls the function that saves data to a csv file.
    """
    # Retrieve the typed in name.
    fileName = saveName.get()
    # Check wether dfName is specified.
    if not dfName.empty:
        # Check wether fileName is filled in.
        if fileName != '':
            # Call save function.
            saveData(dfName, fileName)
            saveButton.configure(text="You have already saved this.",
                state='disabled')
            messagebox.showinfo(
                message='You have successfully saved the dataframe to CSV.')
            emptyWidgets(widgetDictList)
        else:
            messagebox.showerror(message='New name is empty!')
    else:
        messagebox.showerror(message='Dataframe is empty!')

def showData(dfName, previewLabel, shapeLabel, buttonToChange=None, justLook=False):
    """
    This function updates certain labels to show the data.
    """
    if justLook:
        previewLabel.configure(text=dfName.head())
        shapeLabel.configure(text=dfName.shape)
    else:
        if buttonToChange:
            previewLabel.configure(text=dfName.head())
            shapeLabel.configure(text=dfName.shape)
            buttonToChange.configure(text='Save the new dataframe to CSV.',
                state='normal')
        else:
            messagebox.showerror(message='No button specified.')

def showHideFrames(hideList=None, showList=None):
    """
    This function removes the frames in the first parameter,
    and shows the one in the second.
    """
    if hideList is not None:
        for frame in hideList:
            frame.grid_remove()
    else:
        pass
    if showList is not None:
        for frame in showList:
            frame.grid()
    else:
        pass

def disableWidget(name, type):
    """
    Disables the widget specified. Only supports the button type.
    Can be expanded to support other widgets.
    """
    if type == 'button':
        name.configure(
            text='Select a function from\nthe dropdown menu!',
            state='disabled')
    else:
        pass

def isInt(x):
    try:
        x = int(x)
        return True
    except:
        return False

def emptyWidgets(listOfDicts, key1='widget', key2='type', key3='special'):
    """
    Function that empties the widget specified.

    Requires a dictionary with the name and type of widget,
    when type is 'entry' it also requires a key named 'special'.
    This key has a boolean and when true, will fill the entry with the path
    pointing to the data folder.
    """
    if isinstance(key1, str) and isinstance(key2, str):
        # Loop over the dictionaries.
        for dict in listOfDicts:
            # Check what whidget type.
            if dict[key2] == 'entry' or dict[key2] == 'listbox':
                dict[key1].delete(0, 'end')
                # Check wether type is entry.
                if dict[key2] == 'entry':
                    # Check wether special is true.
                    if dict[key3]:
                        dict[key1].insert(0, 'data/')
                    else:
                        continue
                else:
                    continue
            elif dict[key2] == 'textbox':
                dict[key1].delete(1.0, 'end')
            elif dict[key2] == 'label':
                dict[key1].configure(text='')
    else:
        pass
