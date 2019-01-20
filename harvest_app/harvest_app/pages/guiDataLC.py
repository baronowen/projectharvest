import tkinter as tk
from tkinter import messagebox
import pandas as pd
pd.options.display.max_columns = 50
import sys

sys.path.append('../')

from harvest_app.functionsM import data_cleaning, guiFunctions

class DataLCPage(tk.Frame):
    """
    Creates the page for data loading and cleaning.
    """
    padx=5
    pady=5
    color = "#FF8000"
    color2 = "#1CC2E5"

    df = pd.DataFrame()
    dfTemp = pd.DataFrame()
    colList = []
    choicesCleaning = {'0': '',
        '1': 'Drop columns',
        '2': 'Drop empty columns',
        '3': 'Copy and drop',
        '4': 'Fill empty columns',
        '5': 'Stringify',
        '6': 'Rename column',
        '7': 'Remove whitespaces',
        '8': 'Shorten postcode'}

    def __init__(self, parent, controller):
        """
        Initializes the actual page.
        Creates the navigation widgets and the frames for the other widgets.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, fg='white', bg='black',
            text="Data loading and cleaning page")
        label.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# NavFrame------------------------------------------------------------------------------
        navFrame = tk.Frame(self, bg=self.color, bd=10)
        navFrame.grid(column=0, row=1, columnspan=2, sticky='NSWE')

        buttonM = tk.Button(navFrame, text="Go to Merge page",
            command=lambda: controller.show_frame("MergePage"))
        buttonM.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        buttonManip = tk.Button(navFrame, text="Go to Data Manipulation page",
            command=lambda: controller.show_frame("DataManipPage"))
        buttonManip.grid(column=2, row=0, padx=self.padx, pady=self.pady)

        buttonCluster = tk.Button(navFrame, text="Go to Cluster page",
            command=lambda: controller.show_frame("ClusteringPage"))
        buttonCluster.grid(column=3, row=0, padx=self.padx, pady=self.pady)

        buttonAdwords = tk.Button(navFrame, text="Go to Adwords page",
            command=lambda: controller.show_frame("AdwordsPage"))
        buttonAdwords.grid(column=4, row=0, padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
        self.leftFrame = tk.Frame(self, bg=self.color, bd=10)
        self.leftFrame.grid(column=0, row=3, sticky='NSEW')

        self.rightFrame = tk.Frame(self, bg=self.color, bd=10)
        self.rightFrame.grid(column=1, row=3, sticky='NSEW')

        self.clearButton = tk.Button(self,
            text='Clear all entry field, text boxes, labels etc',
            command=self.callEmptyWidgets)
        self.clearButton.grid(column=0, row=2, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.widgets()

    def widgets(self):
        """
        Creating the widgets that do the loading and cleaning.
        """
# LoadingFrame------------------------------------------------------------------------------
        loadingFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        loadingFrame.grid(column=0, row=0, sticky='NS')

        pathLabel = tk.Label(loadingFrame, text="Path to file: ")
        pathLabel.grid(column=0, row=1, sticky='W',
            padx=self.padx, pady=self.pady)

        self.pathEntry = tk.Entry(loadingFrame, width=25)
        self.pathEntry.insert(0, 'data/')
        self.pathEntry.grid(column=1, row=1, sticky='E',
            padx=self.padx, pady=self.pady)

        typeLabel = tk.Label(loadingFrame, text="File type: ")
        typeLabel.grid(column=0, row=2, sticky='W',
            padx=self.padx, pady=self.pady)

        self.typeVar = tk.StringVar()

        typeExcel = tk.Radiobutton(loadingFrame, text='Excel',
                                variable=self.typeVar,
                                value='.xlsx')
        typeCsv = tk.Radiobutton(loadingFrame, text='CSV',
                                variable=self.typeVar,
                                value='.csv')
        self.typeVar.set(value='.xlsx')
        typeExcel.grid(column=1, row=2, sticky='W',
            padx=self.padx, pady=self.pady)
        typeCsv.grid(column=1, row=2, sticky='E',
            padx=self.padx, pady=self.pady)

        button = tk.Button(loadingFrame, text="Load file",
            command=self.triggerLoadingData)
        button.grid(column=1, row=3, sticky='EW',
            padx=self.padx, pady=self.pady)
# DropDownFrame------------------------------------------------------------------------------
        dropdownFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        dropdownFrame.grid(column=1, row=0, sticky='NS')


        dropLabelC = tk.Label(dropdownFrame, text="Data cleaning\nfunctions:")
        dropLabelC.grid(column=0, row=1, sticky='W',
            padx=self.padx, pady=self.pady)

        self.dropCVar = tk.StringVar()
        optionsC = ['', 'Drop columns', 'Drop empty columns', 'Copy and drop',
            'Fill empty columns', 'Stringify', 'Rename column',
            'Remove whitespaces', 'Shorten postcode']
        dropClean = tk.OptionMenu(dropdownFrame, self.dropCVar, *optionsC,
            command=self.changeDropC)
        dropClean.grid(column=1, row=1, sticky='E',
            padx=self.padx, pady=self.pady)
# CleanFrame------------------------------------------------------------------------------
        cleanGenericFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        cleanGenericFrame.grid(column=0, row=1, columnspan=2, sticky='N')

        self.cleanButton = tk.Button(cleanGenericFrame,
            text='Select a function\nfrom the dropdown menu!',
            state='disabled')
        self.cleanButton.grid(column=0, row=3, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.dropFrame = tk.Frame(cleanGenericFrame, bg=self.color2, bd=10)
        self.dropFrame.grid(column=0, row=1, sticky='NS')
        self.dropFrame.grid_remove()
        self.dropLabel = tk.Label(self.dropFrame,
            text="Select the columns you wish to drop:")
        self.dropLabel.grid(column=0, row=0, sticky='WE',
            padx=self.padx, pady=self.pady)

        self.dropList = tk.Listbox(self.dropFrame, selectmode='multiple',
            exportselection=1)
        self.dropList.grid(column=0, row=1, padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.copyFrame = tk.Frame(cleanGenericFrame, bg=self.color2, bd=10)
        self.copyFrame.grid(column=1, row=1, sticky='NS')
        self.copyFrame.grid_remove()
        copyDropLabel = tk.Label(self.copyFrame,
            text='Select columns you wish to drop:')
        copyDropLabel.grid(column=0, row=0, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.copyDropList = tk.Listbox(self.copyFrame, selectmode='multiple',
            exportselection=0)
        self.copyDropList.grid(column=0, row=1, columnspan=2,
            padx=self.padx, pady=self.pady)

        copyDropNameLabel = tk.Label(self.copyFrame, text="Name of copy:")
        copyDropNameLabel.grid(column=0, row=2,
            padx=self.padx, pady=self.pady)

        self.copyDropNameEntry = tk.Entry(self.copyFrame, width=20)
        self.copyDropNameEntry.grid(column=1, row=2,
            padx=self.padx, pady=self.pady)

        copyDropNotice = tk.Label(self.copyFrame,
            text='File extension is not required!\n'
                'Copies will automatically\nbe stored as CSV files.')
        copyDropNotice.grid(column=0, row=3, columnspan=2,
            padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.fillFrame = tk.Frame(cleanGenericFrame, bg=self.color2, bd=10)
        self.fillFrame.grid(column=0, row=2, sticky='NS')
        self.fillFrame.grid_remove()
        fillLabel = tk.Label(self.fillFrame,
            text="The value you wish to\nfill the columns with:")
        fillLabel.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        self.fillEntry = tk.Entry(self.fillFrame, width=10)
        self.fillEntry.grid(column=1, row=0, padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.renameFrame = tk.Frame(cleanGenericFrame, bg=self.color2, bd=10)
        self.renameFrame.grid(column=0, row=2)
        self.renameFrame.grid_remove()
        renameLabel = tk.Label(self.renameFrame, text="New column name:")
        renameLabel.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        self.renameEntry = tk.Entry(self.renameFrame, width=25)
        self.renameEntry.grid(column=1, row=0, padx=self.padx, pady=self.pady)
# PreviewFrame------------------------------------------------------------------------------
        previewFrame = tk.Frame(self.rightFrame, bg=self.color2, bd=10)
        previewFrame.grid(column=0, row=0)

        self.previewLabel2 = tk.Label(previewFrame)
        self.previewLabel2.grid(column=0, row=1,
            padx=self.padx, pady=self.pady)

        shapeLabel = tk.Label(previewFrame, text='Shape of the data (rows, columns)')
        shapeLabel.grid(column=0, row=2,
            padx=self.padx, pady=self.pady)

        self.shapeLabel2 = tk.Label(previewFrame)
        self.shapeLabel2.grid(column=0, row=3,
            padx=self.padx, pady=self.pady)
# SaveFrame------------------------------------------------------------------------------
        saveFrame = tk.Frame(self.rightFrame, bg=self.color2, bd=10)
        saveFrame.grid(column=0, row=2)

        saveLabel = tk.Label(saveFrame, text='Name of the new file:')
        saveLabel.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        self.saveName = tk.Entry(saveFrame, width=20)
        self.saveName.grid(column=1, row=0,
            padx=self.padx, pady=self.pady)

        self.saveButton = tk.Button(saveFrame,
            text='Save the new dataframe to CSV.',
            command=lambda: guiFunctions.saveDataframe(self.saveName,
                self.df, self.saveButton, [{'widget': self.saveName,
                                            'type': 'entry', 'special': False}]),
            state='disabled')
        self.saveButton.grid(column= 0, row=1, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
    def callEmptyWidgets(self):
        self.df = pd.DataFrame()
        self.dfTemp = pd.DataFrame()
        self.colList.clear()
        guiFunctions.emptyWidgets(
            [{'widget': self.previewLabel2, 'type': 'label'},
            {'widget': self.shapeLabel2, 'type': 'label'},
            {'widget': self.saveName, 'type': 'entry', 'special': False},
            {'widget': self.pathEntry, 'type': 'entry', 'special': True},
            {'widget': self.dropList, 'type': 'listbox'},
            {'widget': self.copyDropList, 'type': 'listbox'},
            {'widget': self.copyDropNameEntry, 'type': 'entry', 'special': False},
            {'widget': self.fillEntry, 'type': 'entry', 'special': False},
            {'widget': self.renameEntry, 'type': 'entry', 'special': False}])

    def changeDropC(self, value):
        """Function that shows different frames dependent on the choice made."""
        menuItem = value
        choices = self.choicesCleaning
        if menuItem == choices['0']:
            self.noChoiceMade()
        elif menuItem == choices['1']:
            self.choseDrop1()
        elif menuItem == choices['2']:
            self.choseDrop2()
        elif menuItem == choices['3']:
            self.choseCopyAndDrop()
        elif menuItem == choices['4']:
            self.choseFill()
        elif menuItem == choices['5']:
            self.choseString()
        elif menuItem == choices['6']:
            self.choseRename()
        elif menuItem == choices['7']:
            self.choseRemoveW()
        elif menuItem == choices['8']:
            self.choseShortenPostcode()

    def noChoiceMade(self):
        """
        Remove all cleaning frames and disable the clean button.
        """
        guiFunctions.showHideFrames([self.dropFrame, self.copyFrame,
            self.fillFrame, self.renameFrame])
        guiFunctions.disableWidget(self.cleanButton, 'button')

    def choseDrop1(self):
        """
        Show frame needed to drop columns and enable the button.
        """
        guiFunctions.showHideFrames([self.copyFrame,
            self.fillFrame, self.renameFrame], [self.dropFrame])
        self.dropLabel.configure(
            text='Select the columns you wish to drop:')
        self.dropList.configure(selectmode='multiple',
            exportselection=1)
        self.cleanButton.configure(
            text='Drop columns',
            state='normal',
            command=self.execDrop1)

    def execDrop1(self):
        """Execute the drop function on button click."""
        # Retrieve selected columns.
        items = guiFunctions.retrieveItems(self.dropList, 'listBox')
        # Call drop function.
        self.dfTemp = data_cleaning.dropColumns(self.df, True, items)
        # Check if a string is returned.
        if isinstance(self.dfTemp, str):
            messagebox.showerror(message=self.dfTemp)
        else:
            self.df = self.dfTemp
            # Show the data and enable the save button.
            guiFunctions.showData(self.df,
                self.previewLabel2, self.shapeLabel2,
                self.saveButton)
            # Refresh the list boxes.
            guiFunctions.refreshLists(self.df,
                [self.dropList, self.copyDropList])
            # Hide the frame.
            guiFunctions.showHideFrames([self.copyFrame,
                self.fillFrame, self.renameFrame, self.dropFrame])
            # Disable clean button.
            guiFunctions.disableWidget(self.cleanButton,
                'button')
            # Reset drop down.
            self.dropCVar.set('')

    def choseDrop2(self):
        """Function that shows and configures widget for Dropping empty columns."""
        guiFunctions.showHideFrames([self.copyFrame,
            self.fillFrame, self.renameFrame], [self.dropFrame])
        self.dropLabel.configure(
            text='Select columns to drop:\nOnly empty ones will be dropped!')
        self.dropList.configure(selectmode='multiple',
            exportselection=1)
        self.cleanButton.configure(
            text='Drop empty columns only',
            state='normal',
            command=self.execDrop2)

    def execDrop2(self):
        """Executing drop empty columns on button click."""
        items = guiFunctions.retrieveItems(self.dropList, 'listBox')
        # Dropping columns
        self.dfTemp = data_cleaning.dropColumns(self.df, False, items)
        # Check what is returned.
        if isinstance(self.dfTemp, str):
            messagebox.showerror(message=self.dfTemp)
        else:
            self.df = self.dfTemp
            # Showing the data.
            guiFunctions.showData(self.df,
                self.previewLabel2, self.shapeLabel2,
                self.saveButton)
            # Refreshing the list boxes.
            guiFunctions.refreshLists(self.df,
                [self.dropList, self.copyDropList])
            # Hide frames.
            guiFunctions.showHideFrames([self.copyFrame,
                self.fillFrame, self.renameFrame, self.dropFrame])
            # Disable clean button.
            guiFunctions.disableWidget(self.cleanButton,
                'button')
            # Reset drop down.
            self.dropCVar.set('')

    def choseCopyAndDrop(self):
        """Function that shows widget needed to copy and drop certain columns."""
        guiFunctions.showHideFrames([self.fillFrame,
            self.renameFrame], [self.dropFrame, self.copyFrame])
        self.dropLabel.configure(
            text='Select columns you wish to copy:')
        self.dropList.configure(selectmode='multiple',
            exportselection=0)
        self.cleanButton.configure(
            text='Copy and drop columns.',
            state='normal',
            command=self.execCopyAndDrop)

    def execCopyAndDrop(self):
        """Function that executes the copying and dropping."""
        copy = guiFunctions.retrieveItems(self.dropList, 'listBox')
        drop = guiFunctions.retrieveItems(self.copyDropList, 'listBox')
        name = self.copyDropNameEntry.get()
        # Call the function.
        self.dfTemp = data_cleaning.copyAndDrop(self.df, copy, drop, name)
        # Check what is returned.
        if isinstance(self.dfTemp, str):
            messagebox.showerror(message=self.dfTemp)
        else:
            self.df = self.dfTemp
            # Show the data.
            guiFunctions.showData(self.df,
                self.previewLabel2, self.shapeLabel2,
                self.saveButton)
            # Refresh the list boxes.
            guiFunctions.refreshLists(self.df,
                [self.dropList, self.copyDropList])
            list = [{'widget': self.copyDropNameEntry, 'type': 'entry', 'special': False}]
            # Empty the widgets in the list above.
            guiFunctions.emptyWidgets(list)
            # Hide frames
            guiFunctions.showHideFrames([self.copyFrame,
                self.fillFrame, self.renameFrame, self.dropFrame])
            # Disable clean button.
            guiFunctions.disableWidget(self.cleanButton,
                'button')
            self.dropCVar.set('')
            messagebox.showinfo(message='Succesfully copied and dropped selected columns.')

    def choseFill(self):
        """Function that shows shows widget needed to fill empty columns."""
        guiFunctions.showHideFrames([self.copyFrame,
            self.renameFrame], [self.dropFrame, self.fillFrame])
        self.dropLabel.configure(
            text='Select columns you wish to fill:')
        self.dropList.configure(selectmode='multiple',
            exportselection=0)
        self.cleanButton.configure(
            text='Fill columns.',
            state='normal',
            command=self.execFill)

    def execFill(self):
        """Function that executes the fill empty columns function."""
        items = guiFunctions.retrieveItems(self.dropList, 'listBox')
        fill = self.fillEntry.get()
        # Call the function.
        self.dfTemp = data_cleaning.fillEmptyColumns(self.df, fill, items)
        # Check what was returned.
        if isinstance(self.dfTemp, str):
            messagebox.showerror(message=self.dfTemp)
        else:
            self.df = self.dfTemp
            # Show data.
            guiFunctions.showData(self.df, self.previewLabel2,
                self.shapeLabel2, self.saveButton)
            # Refresh list boxes.
            guiFunctions.refreshLists(self.df,
                [self.dropList, self.copyDropList])
            # Empty widgets in list.
            list = [{'widget': self.fillEntry, 'type': 'entry', 'special': False}]
            guiFunctions.emptyWidgets(list)
            # Hide frames.
            guiFunctions.showHideFrames([self.copyFrame,
                self.fillFrame, self.renameFrame, self.dropFrame])
            guiFunctions.disableWidget(self.cleanButton,
                'button')
            self.dropCVar.set('')

    def choseString(self):
        """Function that shows widgets needed to stringify."""
        guiFunctions.showHideFrames([self.copyFrame,
            self.fillFrame, self.renameFrame], [self.dropFrame])
        self.dropLabel.configure(
            text='Select columns you wish to convert to string:')
        self.dropList.configure(selectmode='multiple',
            exportselection=1)
        self.cleanButton.configure(
            text='Stringify columns.',
            state='normal',
            command=self.execString)

    def execString(self):
        """Execute stringify."""
        items = guiFunctions.retrieveItems(self.dropList, 'listBox')
        self.dfTemp = data_cleaning.stringify(self.df, items)
        if isinstance(self.dfTemp, str):
            messagebox.showerror(message=self.dfTemp)
        else:
            self.df = self.dfTemp
            guiFunctions.showData(self.df, self.previewLabel2,
                self.shapeLabel2, self.saveButton)
            guiFunctions.refreshLists(self.df,
                [self.dropList, self.copyDropList])
            guiFunctions.showHideFrames([self.copyFrame,
                self.fillFrame, self.renameFrame, self.dropFrame])
            guiFunctions.disableWidget(self.cleanButton,
                'button')
            self.dropCVar.set('')
            messagebox.showinfo(message='Stringified selected column(s).')

    def choseRename(self):
        """Show widgets to rename a column."""
        guiFunctions.showHideFrames([self.copyFrame, self.fillFrame],
            [self.dropFrame, self.renameFrame])
        self.dropLabel.configure(
            text="Select the column you wish to rename:")
        self.dropList.configure(selectmode='single',
            exportselection=0)
        self.cleanButton.configure(
            text="Rename column",
            state='normal',
            command=self.execRename)

    def execRename(self):
        """Rename a column."""
        try:
            items = guiFunctions.retrieveItems(self.dropList, 'listBox')
            item = items[0]
            newName = self.renameEntry.get()
            self.dfTemp = data_cleaning.rename(self.df, item, newName)
            if isinstance(self.dfTemp, str):
                messagebox.showerror(message=self.dfTemp)
            else:
                self.df = self.dfTemp
                guiFunctions.showData(self.df, self.previewLabel2,
                    self.shapeLabel2, self.saveButton)
                guiFunctions.refreshLists(self.df,
                    [self.dropList, self.copyDropList])
                list = [{'widget': self.renameEntry, 'type': 'entry', 'special': False}]
                guiFunctions.emptyWidgets(list)
                guiFunctions.showHideFrames([self.copyFrame,
                    self.fillFrame, self.renameFrame, self.dropFrame])
                guiFunctions.disableWidget(self.cleanButton,
                    'button')
                self.dropCVar.set('')
        except IndexError:
            messagebox.showerror(message='Select a column!')

    def choseRemoveW(self):
        """Show widgets to remove whitespaces from columns."""
        guiFunctions.showHideFrames([self.copyFrame, self.fillFrame,
            self.renameFrame], [self.dropFrame])
        self.dropLabel.configure(
            text="Select the columns where"
                "\nyou wish to remove whitespaces:")
        self.dropList.configure(selectmode='multiple',
            exportselection=1)
        self.cleanButton.configure(text="Remove whitespaces",
            state='normal',
            command=self.execRemoveW)

    def execRemoveW(self):
        """"Remove whitespaces from columns."""
        items = guiFunctions.retrieveItems(self.dropList, 'listBox')
        self.dfTemp = data_cleaning.removeW(self.df, items)
        if isinstance(self.dfTemp, str):
            messagebox.showerror(message=self.dfTemp)
        else:
            self.df = self.dfTemp
            guiFunctions.showData(self.df, self.previewLabel2,
                self.shapeLabel2, self.saveButton)
            guiFunctions.refreshLists(self.df,
                [self.dropList, self.copyDropList])
            guiFunctions.showHideFrames([self.copyFrame,
                self.fillFrame, self.renameFrame, self.dropFrame])
            guiFunctions.disableWidget(self.cleanButton,
                'button')
            self.dropCVar.set('')
            messagebox.showinfo(message='Removed whitespaces.')

    def choseShortenPostcode(self):
        """Show widgets to shorten a postcode."""
        guiFunctions.showHideFrames([self.copyFrame, self.fillFrame,
            self.renameFrame], [self.dropFrame])
        self.dropLabel.configure(text="Select the column containing long"
            "\npostcodes to shorten the postcodes")
        self.dropList.configure(selectmode='single')
        self.cleanButton.configure(
            text="Shorten postcode",
            state='normal',
            command=self.execShortenPostcode)

    def execShortenPostcode(self):
        """
        Shorten a postcode.
        Also checks wether selection is valid.
        """
        try:
            items = guiFunctions.retrieveItems(self.dropList, 'listBox')
            item = items[0]
            self.dfTemp = data_cleaning.shortenPostcode(self.df, item)
            if isinstance(self.dfTemp, str):
                messagebox.showerror(message=self.dfTemp)
            else:
                self.df = self.dfTemp
                guiFunctions.showData(self.df, self.previewLabel2,
                    self.shapeLabel2, self.saveButton)
                guiFunctions.showHideFrames([self.copyFrame,
                    self.fillFrame, self.renameFrame, self.dropFrame])
                guiFunctions.disableWidget(self.cleanButton,
                    'button')
                self.dropCVar.set('')
        except IndexError:
            messagebox.showerror(message='Select the column containing postcodes!')
# ******************************************************************************
    def triggerLoadingData(self):
        self.df = guiFunctions.loadingData(self.pathEntry,
            self.typeVar, 'dataLC', listboxes=[self.dropList,
            self.copyDropList], previewLabel=self.previewLabel2,
            shapeLabel=self.shapeLabel2, saveButton=self.saveButton)
