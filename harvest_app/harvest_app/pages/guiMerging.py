import tkinter as tk
import pandas as pd
pd.options.display.max_columns = 50
import sys
sys.path.append('../')

from harvest_app.functionsM import dataLoading, dataManipFunctions, guiFunctions

class MergePage(tk.Frame):
    """The page to merge two dataframes together."""
    padx=5
    pady=5
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    color = "#FF8000"
    color2 = "#1CC2E5"

    def __init__(self, parent, controller):
        """The constructor that initializes the page."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, fg='white', bg='black', text="Merge page")
        label.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# NavFrame------------------------------------------------------------------------------
        navFrame = tk.Frame(self, bg=self.color, bd=10)
        navFrame.grid(column=0, row=1, columnspan=2, sticky='WE')

        buttonM = tk.Button(navFrame, text="Go to Data Loading and Cleaning page",
            command=lambda: controller.show_frame("DataLCPage"))
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
        self.topFrame = tk.Frame(self, bg=self.color, bd=10)
        self.topFrame.grid(column=0, row=3, sticky='NSWE')

        self.bottomFrame = tk.Frame(self, bg=self.color, bd=10)
        self.bottomFrame.grid(column=0, row=4, sticky='NS')

        self.clearButton = tk.Button(self,
            text='Clear all entry field, text boxes, labels etc',
            command=self.callEmptyWidgets)
        self.clearButton.grid(column=0, row=2, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.widgets()

    def widgets(self):
        """The function that creates all widgets."""
        loadingFrame = tk.Frame(self.topFrame, bg=self.color2, bd=10)
        loadingFrame.grid(column=0, row=0)
# DataLoadingFrame------------------------------------------------------------------------
        loadingFrame1 = tk.Frame(loadingFrame, bg=self.color2, bd=10)
        loadingFrame1.grid(column=0, row=0)

        loadingLabel1 = tk.Label(loadingFrame1, text="Data 1:")
        loadingLabel1.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)

        pathLabel1 = tk.Label(loadingFrame1, text="Path to file:")
        pathLabel1.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        self.pathEntry1 = tk.Entry(loadingFrame1, width=25)
        self.pathEntry1.insert(0, 'data/')
        self.pathEntry1.grid(column=1, row=1, padx=self.padx, pady=self.pady)

        typeLabel1 = tk.Label(loadingFrame1, text="File type:")
        typeLabel1.grid(column=0, row=2, padx=self.padx, pady=self.pady)

        self.typeVar1 =tk.StringVar()
        typeExcel1 = tk.Radiobutton(loadingFrame1, text='Excel',
                                variable=self.typeVar1,
                                value='.xlsx')
        typeCsv1 = tk.Radiobutton(loadingFrame1, text='CSV',
                                variable=self.typeVar1,
                                value='.csv')
        self.typeVar1.set(value='.xlsx')
        typeExcel1.grid(column=1, row=2, sticky='W',
            padx=self.padx, pady=self.pady)
        typeCsv1.grid(column=1, row=2, sticky='E',
            padx=self.padx, pady=self.pady)

        loadButton1 = tk.Button(loadingFrame1, text="Load file",
            command=lambda: self.triggerLoadingData(bool=True))
        loadButton1.grid(column=1, row=3, sticky='WE',
            padx=self.padx, pady=self.pady)
# ******************************************************************************
        loadingFrame2 = tk.Frame(loadingFrame, bg=self.color2, bd=10)
        loadingFrame2.grid(column=0, row=1)

        loadingLabel2 = tk.Label(loadingFrame2, text="Data 2:")
        loadingLabel2.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)

        pathLabel2 = tk.Label(loadingFrame2, text="Path to file:")
        pathLabel2.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        self.pathEntry2 = tk.Entry(loadingFrame2, width=25)
        self.pathEntry2.insert(0, 'data/')
        self.pathEntry2.grid(column=1, row=1, padx=self.padx, pady=self.pady)

        typeLabel1 = tk.Label(loadingFrame1, text="File type:")
        typeLabel1.grid(column=0, row=2, padx=self.padx, pady=self.pady)

        self.typeVar2 =tk.StringVar()
        typeExcel2 = tk.Radiobutton(loadingFrame2, text='Excel',
                                variable=self.typeVar2,
                                value='.xlsx')
        typeCsv2 = tk.Radiobutton(loadingFrame2, text='CSV',
                                variable=self.typeVar2,
                                value='.csv')
        self.typeVar2.set(value='.xlsx')
        typeExcel2.grid(column=1, row=2, sticky='W',
            padx=self.padx, pady=self.pady)
        typeCsv2.grid(column=1, row=2, sticky='E',
            padx=self.padx, pady=self.pady)

        loadButton2 = tk.Button(loadingFrame2, text="Load file",
            command=lambda: self.triggerLoadingData(bool=False))
        loadButton2.grid(column=1, row=3, sticky='WE',
            padx=self.padx, pady=self.pady)
# MergeFrame------------------------------------------------------------------------------
        mergeFrame = tk.Frame(self.topFrame, bg=self.color2, bd=10)
        mergeFrame.grid(column=1, row=0, sticky='NS')

        columnsLabel1 = tk.Label(mergeFrame, text="Columns data 1:")
        columnsLabel1.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        self.columnsList1 = tk.Listbox(mergeFrame, exportselection=0)
        self.columnsList1.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        mergeButton = tk.Button(mergeFrame,
            text="Merge the left with the right",
            command=self.merge)
        mergeButton.grid(column=1, row=1, sticky='S',
            padx=self.padx, pady=self.pady)

        columnsLabel2 = tk.Label(mergeFrame, text="Columns data 2:")
        columnsLabel2.grid(column=2, row=0, padx=self.padx, pady=self.pady)

        self.columnsList2 = tk.Listbox(mergeFrame, exportselection=0)
        self.columnsList2.grid(column=2, row=1, padx=self.padx, pady=self.pady)

        columnsLabel2 = tk.Label(mergeFrame,
            text="Select the column you wish to merge on in both list boxes.")
        columnsLabel2.grid(column=0, row=2, columnspan=3, sticky='WE',
            padx=self.padx, pady=self.pady)
# PreviewFrame------------------------------------------------------------------------------
        previewFrame = tk.Frame(self.bottomFrame, bg=self.color2, bd=10)
        previewFrame.grid(column=0, row=0, sticky='NSW')

        # previewLabel = tk.Label(previewFrame, text="Preview frame:")
        # previewLabel.grid(column=0, row=0, sticky='WE',
        #     padx=self.padx, pady=self.pady)

        self.previewLabel2 = tk.Label(previewFrame)
        self.previewLabel2.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        shapeLabel = tk.Label(previewFrame, text="Shape of the data (rows, columns)")
        shapeLabel.grid(column=0, row=2, padx=self.padx, pady=self.pady)

        self.shapeLabel2 = tk.Label(previewFrame)
        self.shapeLabel2.grid(column=0, row=3, padx=self.padx, pady=self.pady)
# SaveFrame------------------------------------------------------------------------------
        saveFrame = tk.Frame(self.bottomFrame, bg=self.color2, bd=10)
        saveFrame.grid(column=1, row=0, sticky='NSE')

        saveLabel = tk.Label(saveFrame, text="Name of the new file:")
        saveLabel.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        self.saveName = tk.Entry(saveFrame, width=20)
        self.saveName.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        self.saveButton = tk.Button(saveFrame,
            text="Save the new dataframe to CSV.",
            command=lambda: guiFunctions.saveDataframe(self.saveName,
                self.df3, self.saveButton, [{'widget': self.saveName,
                    'type': 'entry', 'special': False}]),
            state='disabled')
        self.saveButton.grid(column=0, row=1, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
    def callEmptyWidgets(self):
        self.df1 = pd.DataFrame()
        self.df2 = pd.DataFrame()
        self.df3 = pd.DataFrame()
        guiFunctions.emptyWidgets(
            [{'widget': self.previewLabel2, 'type': 'label'},
            {'widget': self.shapeLabel2, 'type': 'label'},
            {'widget': self.saveName, 'type': 'entry', 'special': False},
            {'widget': self.pathEntry1, 'type': 'entry', 'special': True},
            {'widget': self.pathEntry2, 'type': 'entry', 'special': True},
            {'widget': self.columnsList1, 'type': 'listbox'},
            {'widget': self.columnsList2, 'type': 'listbox'}])

    def triggerLoadingData(self, bool):
        if bool:
            self.df1 = guiFunctions.loadingData(self.pathEntry1,
                self.typeVar1, 'merging', listboxes=[self.columnsList1],
                bool=bool)
        elif not bool:
            self.df2 = guiFunctions.loadingData(self.pathEntry2,
                self.typeVar2, 'merging', listboxes=[self.columnsList2],
                bool=bool)

    def merge(self):
        """Function that calls the merge function."""
        try:
            # Retrieve the selected columns.
            leftOn = guiFunctions.retrieveItems(self.columnsList1, 'listBox')
            leftOn = leftOn[0]
            rightOn = guiFunctions.retrieveItems(self.columnsList2, 'listBox')
            rightOn = rightOn[0]
            # Checking if columns were selected.
            if leftOn:
                if rightOn:
                    # Check if the selected columns have the same name.
                    if leftOn == rightOn:
                        # Merge on 1 column.
                        self.df3 = dataManipFunctions.mergeDataframes(
                            self.df1, self.df2, mergeOn=leftOn)
                        if isinstance(self.df3, str):
                            messagebox.showerror(message=self.dfTemp)
                        else:
                            guiFunctions.showData(self.df3,
                                self.previewLabel2, self.shapeLabel2,
                                self.saveButton)
                    else:
                        # Merge with leftOn and rightOn specified.
                        self.df3 = dataManipFunctions.mergeDataframes(
                            self.df1, self.df2, leftOn=leftOn, rightOn=rightOn)
                        if isinstance(self.df3, str):
                            messagebox.showerror(message=self.dfTemp)
                        else:
                            guiFunctions.showData(self.df3,
                                self.previewLabel2, self.shapeLabel2,
                                self.saveButton)
                else:
                    messagebox.showerror(
                        message='Select a column from the right dataframe!')
            else:
                messagebox.showerror(
                    message='Select a column from the left dataframe!')
        except IndexError:
            messagebox.showerror(message='No columns selected!')
