import tkinter as tk
from tkinter import messagebox
import pandas as pd
pd.options.display.max_columns = 50
import sys
sys.path.append('../')

from harvest_app.functionsM import guiFunctions, dataManipFunctions

class DataManipPage(tk.Frame):
    """
    The page for data manipulation.

    Includes functions to encode a column,
    extract conversions an calculate percentages.
    """
    padx=5
    pady=5
    df = pd.DataFrame()
    dfC = pd.DataFrame()
    dfTemp = pd.DataFrame()
    colList = []
    colListC = []
    choicesManip = {
        '0': '',
        '1': 'Extract Potential Conversions',
        '2': 'Encode Column',
        '3': 'Calculate percentages'
    }
    color = "#FF8000"
    color2 = "#1CC2E5"

    def __init__(self, parent, controller):
        """Constructor that initializes the page."""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, fg='white', bg='black',
            text="Data Manipulation Page")
        label.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# NavFrame------------------------------------------------------------------------------
        navFrame = tk.Frame(self, bg=self.color, bd=10)
        navFrame.grid(column=0, row=1, columnspan=2, sticky='WE')

        buttonDLC = tk.Button(navFrame,
            text="Go to Data Loading and Cleaning page",
            command=lambda: controller.show_frame("DataLCPage"))
        buttonDLC.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        buttonM = tk.Button(navFrame, text="Go to Merge page",
            command=lambda: controller.show_frame("MergePage"))
        buttonM.grid(column=2, row=0, padx=self.padx, pady=self.pady)

        buttonCluster = tk.Button(navFrame, text="Go to Cluster page",
            command=lambda: controller.show_frame("ClusteringPage"))
        buttonCluster.grid(column=3, row=0, padx=self.padx, pady=self.pady)

        buttonAdwords = tk.Button(navFrame, text="Go to Adwords page",
            command=lambda: controller.show_frame("AdwordsPage"))
        buttonAdwords.grid(column=4, row=0, padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
        self.leftFrame = tk.Frame(self, bg=self.color, bd=10)
        self.leftFrame.grid(column=0, row=3, sticky='NSWE')

        self.rightFrame = tk.Frame(self, bg=self.color, bd=10)
        self.rightFrame.grid(column=1, row=3, sticky='NSEW')

        self.clearButton = tk.Button(self,
            text='Clear all entry field, text boxes, labels etc',
            command=self.callEmptyWidgets)
        self.clearButton.grid(column=0, row=2, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.widgets()

    def widgets(self):
        """"Function that creates the widgets to load and manipulate the data."""
# LoadingFrame----------------------------------------------------------------------------
        loadingFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        loadingFrame.grid(column=0, row=0, sticky='')

        self.loadinglabel = tk.Label(loadingFrame, text="Data loading:")
        self.loadinglabel.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)

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
            command=lambda: self.triggerLoadingData(True))
        button.grid(column=1, row=3, sticky='EW',
            padx=self.padx, pady=self.pady)
# DropdownFrame----------------------------------------------------------------------
        dropdownFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        dropdownFrame.grid(column=0, row=1, sticky='NS')

        dropLabelManip = tk.Label(dropdownFrame,
            text="Data Manipulation\nfunctions:")
        dropLabelManip.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        self.dropManipVar = tk.StringVar()
        optionsManip = ['', 'Extract Potential Conversions', 'Encode Column',
            'Calculate percentages']
        dropManip = tk.OptionMenu(dropdownFrame, self.dropManipVar, *optionsManip,
            command=self.changeDropManip)
        dropManip.grid(column=1, row=1, padx=self.padx, pady=self.pady)
# DataManipulation--------------------------------------------------------------------
        dataManipFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        dataManipFrame.grid(column=0, row=2, sticky='N')

        self.manipButton = tk.Button(dataManipFrame,
            text='Select a function from\nthe dropdown menu',
            state='disabled')
        self.manipButton.grid(column=0, row=2, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.extractFrame = tk.Frame(dataManipFrame, bg=self.color2, bd=10)
        self.extractFrame.grid(column=0, row=1, sticky='NS')
        self.extractFrame.grid_remove()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.extractFrame2 = tk.Frame(dataManipFrame, bg=self.color2, bd=10)
        self.extractFrame2.grid(column=1, row=1, sticky='N')
        self.extractFrame2.grid_remove()
        self.colLabel = tk.Label(self.extractFrame2,
            text="Select the column that\nindicates conversions:")
        self.colLabel.grid(column=0, row=0,
            padx=self.padx, pady=self.pady)

        self.colListbox = tk.Listbox(self.extractFrame2, exportselection=0)
        self.colListbox.grid(column=0, row=1,
            padx=self.padx, pady=self.pady)
# PreviewFrame-------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------
    def callEmptyWidgets(self):
        self.df = pd.DataFrame()
        self.dfC = pd.DataFrame()
        self.dfTemp = pd.DataFrame()
        self.colList.clear()
        self.colListC.clear()
        guiFunctions.emptyWidgets(
            [{'widget': self.previewLabel2, 'type': 'label'},
            {'widget': self.shapeLabel2, 'type': 'label'},
            {'widget': self.saveName, 'type': 'entry', 'special': False},
            {'widget': self.pathEntry, 'type': 'entry', 'special': True},
            {'widget': self.colListbox, 'type': 'listbox'}])

    def changeDropManip(self, value):
        """Call functions that show different widgets dependent on chosen option."""
        menuItem = value
        choices = self.choicesManip
        if menuItem == choices['0']:
            self.noChoiceMadeManip()
        elif menuItem == choices['1']:
            self.choseExtract()
        elif menuItem == choices['2']:
            self.choseEncode()
        elif menuItem == choices['3']:
            self.choseCalculate()

    def noChoiceMadeManip(self):
        """Hide all frames and disable the button."""
        guiFunctions.showHideFrames([self.extractFrame2])

        guiFunctions.disableWidget(self.manipButton, 'button')
        self.loadinglabel.configure(text="Data loading:")

    def choseExtract(self):
        """Show widgets for extracting function."""
        guiFunctions.showHideFrames(showList=[self.extractFrame2])
        self.manipButton.configure(text="Extract conversion numbers",
            state='normal',
            command=self.execExtract)
        self.colLabel.configure(
            text="Select the column that\nindicates conversions:")
        self.colListbox.configure(selectmode='single')
        self.loadinglabel.configure(text="Load conversion data:")

    def execExtract(self):
        """Execute the extract function."""
        try:
            items = guiFunctions.retrieveItems(self.colListbox, 'listBox')
            item = items[0]
            # Calling the function.
            self.dfTemp = dataManipFunctions.extractConv(self.df, item, 'postcode')
            # Checking what is returned.
            if isinstance(self.dfTemp, str):
                messagebox.showerror(message=self.dfTemp)
            else:
                self.df = self.dfTemp
                guiFunctions.showData(self.df, self.previewLabel2,
                    self.shapeLabel2, self.saveButton)
                self.loadinglabel.configure(text="Data loading:")
                guiFunctions.refreshLists(self.df, [self.colListbox])
                guiFunctions.showHideFrames([self.extractFrame2])
                guiFunctions.disableWidget(self.manipButton, 'button')
                self.dropManipVar.set('')
        except IndexError:
            messagebox.showerror(message='Select a column from the list box!')

    def choseEncode(self):
        """Show widgets to encode a column."""
        guiFunctions.showHideFrames(showList=[self.extractFrame2])
        self.manipButton.configure(
            text="Encode selected column",
            state='normal',
            command=self.execEncode)
        self.colLabel.configure(text='Select a column to encode:')
        self.colListbox.configure(selectmode='single')
        self.loadinglabel.configure(text="Data loading:")

    def execEncode(self):
        """Execute the encode function."""
        try:
            items = guiFunctions.retrieveItems(self.colListbox, 'listBox')
            item = items[0]
            # Calling the function.
            self.dfTemp = dataManipFunctions.encodeColumn(self.df, item, item + '1')
            # Checking what is returned.
            if isinstance(self.dfTemp, str):
                messagebox.showerror(message=self.dfTemp)
            else:
                self.df = self.dfTemp
                guiFunctions.showData(self.df, self.previewLabel2,
                    self.shapeLabel2, self.saveButton)
                guiFunctions.refreshLists(self.df,
                    [self.colListbox])
                guiFunctions.showHideFrames([self.extractFrame2])
                guiFunctions.disableWidget(self.manipButton, 'button')
                self.dropManipVar.set('')
        except IndexError:
            messagebox.showerror(message='Select a column from the list box!')

    def choseCalculate(self):
        """"Show widgets to calculate percentages."""
        guiFunctions.showHideFrames(showList=[self.extractFrame2])
        self.manipButton.configure(text="Calculate percentages",
            state='normal',
            command=self.execCalculate)
        self.colLabel.configure(
            text="Select the columns you\nwish to see the conversion"
                "\npercentage of:")
        self.colListbox.configure(selectmode='multiple')
        self.loadinglabel.configure(text="Data loading:")

    def execCalculate(self):
        """Execute the function that calculates the percentages."""
        try:
            items = guiFunctions.retrieveItems(self.colListbox, 'listBox')
            # Calling the function.
            self.dfTemp = dataManipFunctions.calcPercen(self.df, items)
            # Check what is returned.
            if isinstance(self.dfTemp, str):
                messagebox.showerror(message=self.dfTemp)
            else:
                self.df = self.dfTemp
                guiFunctions.showData(self.df, self.previewLabel2,
                    self.shapeLabel2, self.saveButton)
                guiFunctions.showHideFrames([self.extractFrame2])
                guiFunctions.disableWidget(self.manipButton, 'button')
                self.dropManipVar.set('')
        except IndexError:
            messagebox.showerror(message='Select a column from the list box!')
# ******************************************************************************
    def triggerLoadingData(self, bool):
        self.df = guiFunctions.loadingData(self.pathEntry, self.typeVar,
            'dataManip', listboxes=[self.colListbox],
            bool=bool, previewLabel=self.previewLabel2,
            shapeLabel=self.shapeLabel2, saveButton=self.saveButton)
