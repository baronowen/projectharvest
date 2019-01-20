import tkinter as tk
from tkinter import messagebox
import pandas as pd
pd.options.display.max_columns = 50
import sys
sys.path.append('../')

from harvest_app.functionsM import clustering, guiFunctions

class ClusteringPage(tk.Frame):
    """
    Creates the page to cluster the data.

    Can be expanded to support more than just manual clustering.
    """
    padx=5
    pady=5
    color = "#FF8000"
    color2 = "#1CC2E5"
    choicesCl = {'0': '',
        '1': 'Manual'}

    df = pd.DataFrame()
    dfTemp = pd.DataFrame()
    labelList = []

    def __init__(self, parent, controller):
        """
        Constructor, initializes the page by creating the navigation widgets
        and the frames that hold the other widgets.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, fg='white', bg='black', text="Clustering page")
        label.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# NavFrame------------------------------------------------------------------------------
        navFrame = tk.Frame(self, bg=self.color, bd=10)
        navFrame.grid(column=0, row=1, sticky='WE')

        buttonDLC = tk.Button(navFrame,
            text="Go to Data Loading and Cleaning page",
            command=lambda: controller.show_frame("DataLCPage"))
        buttonDLC.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        buttonM = tk.Button(navFrame, text="Go to Merge page",
            command=lambda: controller.show_frame("MergePage"))
        buttonM.grid(column=2, row=0, padx=self.padx, pady=self.pady)

        buttonManip = tk.Button(navFrame, text="Go to Data Manipulation page",
            command=lambda: controller.show_frame("DataManipPage"))
        buttonManip.grid(column=3, row=0, padx=self.padx, pady=self.pady)

        buttonAdwords = tk.Button(navFrame, text="Go to Adwords page",
            command=lambda: controller.show_frame("AdwordsPage"))
        buttonAdwords.grid(column=4, row=0, padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
        self.topFrame = tk.Frame(self, bg=self.color, bd=10)
        self.topFrame.grid(column=0, row=3, sticky='NS')

        self.bottomFrame = tk.Frame(self, bg=self.color, bd=10)
        self.bottomFrame.grid(column=0, row=4, sticky='NS')

        # self.grid_rowconfigure(3, weight=1)
        # self.grid_rowconfigure(4, weight=1)

        self.clearButton = tk.Button(self,
            text='Clear all entry fields, text boxes, labels etc',
            command=self.callEmptyWidgets)
        self.clearButton.grid(column=0, row=2, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.widgets()

    def widgets(self):
        """Function that creates the widgets."""
# LoadingFrame-------------------------------------------------------------------------
        loadingFrame = tk.Frame(self.topFrame, bg=self.color2, bd=10)
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
# DropdownFrame-----------------------------------------------------------------------
        dropdownFrame = tk.Frame(self.topFrame, bg=self.color2, bd=10)
        dropdownFrame.grid(column=1, row=0, sticky='NS')

        dropLabelClu = tk.Label(dropdownFrame, text='Data Clustering:')
        dropLabelClu.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        self.dropClVar = tk.StringVar()
        optionsCl = ['', 'Manual']
        dropCluster = tk.OptionMenu(dropdownFrame, self.dropClVar, *optionsCl,
            command=self.changeDropCluster)
        dropCluster.grid(column=1, row=1, padx=self.padx, pady=self.pady)
# ClusterFrame------------------------------------------------------------------------
        clusterFrame = tk.Frame(self.bottomFrame, bg=self.color2, bd=10)
        clusterFrame.grid(column=0, row=0, sticky='N')

        self.clusterButton = tk.Button(clusterFrame,
            text="Select a function from\nthe dropdown menu!",
            state='disabled')
        self.clusterButton.grid(column=0, row=2, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.manualFrame = tk.Frame(clusterFrame, bg=self.color2, bd=10)
        self.manualFrame.grid(column=0, row=1, columnspan=2)
        self.manualFrame.grid_remove()
        manualLabel = tk.Label(self.manualFrame,
            text="Select the column you wish to cluster on:")
        manualLabel.grid(column=0, row=0, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.manualListBox = tk.Listbox(self.manualFrame, exportselection=0)
        self.manualListBox.grid(column=0, row=1, columnspan=2,
            padx=self.padx, pady=self.pady)

        manualBinsLabel = tk.Label(self.manualFrame,
            text="Type the number of bins\n you wish to create:")
        manualBinsLabel.grid(column=0, row=2, padx=self.padx, pady=self.pady)

        vcmd = (self.register(self.validateBins), '%S')

        self.manualBinsEntry = tk.Entry(self.manualFrame, width=4,
            validate='key', validatecommand=vcmd)
        self.manualBinsEntry.grid(column=1, row=2, padx=self.padx, pady=self.pady)

        manualTextBoxLabel = tk.Label(self.manualFrame,
            text="Type the labels in the box below:")
        manualTextBoxLabel.grid(column=0, row=3, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.manualTextBox = tk.Text(self.manualFrame, state='normal', height=2, width=30)
        self.manualTextBox.grid(column=0, row=4, columnspan=2,
            padx=self.padx, pady=self.pady)

        manualDisclaimer = tk.Label(self.manualFrame,
            text="Labels have to be comma seperated,\n"
                "and the number of labels have to\nmatch with the number of bins!")
        manualDisclaimer.grid(column=0, row=5, columnspan=2,
            padx=self.padx, pady=self.pady)
# PreviewFrame--------------------------------------------------------------------------
        previewFrame = tk.Frame(self.bottomFrame, bg=self.color2, bd=10)
        previewFrame.grid(column=1, row=0, sticky='N')

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
        saveFrame = tk.Frame(self.bottomFrame, bg=self.color2, bd=10)
        saveFrame.grid(column=1, row=1)

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
        self.labelList.clear()
        guiFunctions.emptyWidgets(
            [{'widget': self.previewLabel2, 'type': 'label'},
            {'widget': self.shapeLabel2, 'type': 'label'},
            {'widget': self.saveName, 'type': 'entry', 'special': False},
            {'widget': self.pathEntry, 'type': 'entry', 'special': True},
            {'widget': self.manualListBox, 'type': 'listbox'},
            {'widget': self.manualTextBox, 'type': 'textbox'},
            {'widget': self.manualBinsEntry, 'type': 'entry', 'special': False}])

    def validateBins(self, S):
        """Only allow numbers."""
        if S in '0123456789':
            return True
        else:
            self.bell()
            return False

    def changeDropCluster(self, value):
        """
        Function that shows the necessary frame for the value
        selected in the dropdown menu.
        """
        menuItem = value
        choices = self.choicesCl
        if menuItem == choices['0']:
            self.noChoiceMadeCl()
        elif menuItem == choices['1']:
            self.choseManual()

    def noChoiceMadeCl(self):
        """Hide all frames and disable the button when nothing is selected."""
        guiFunctions.showHideFrames([self.manualFrame])
        guiFunctions.disableWidget(self.clusterButton, 'button')

    def choseManual(self):
        """Show widgets and enable the button for clustering."""
        guiFunctions.showHideFrames(showList=[self.manualFrame])
        self.clusterButton.configure(text="Cluster manually", state='normal',
            command=self.execManual)
        self.manualListBox.configure(selectmode='single')

    def execManual(self):
        """Execute the clustering."""
        try:
            items = guiFunctions.retrieveItems(self.manualListBox, 'listBox')
            item = items[0]
            nBins = self.manualBinsEntry.get()
            if guiFunctions.isInt(nBins):
                nBins = int(nBins)
                self.labelList = guiFunctions.retrieveItems(self.manualTextBox, 'textBox')
                # self.labelList = guiFunctions.retrieveFromTextBox(
                #     self.manualTextBox)
                # Execute cluster function.
                self.dfTemp = clustering.clusterManual(self.df, item, nBins,
                    self.labelList)
                # Check what is returned.
                if isinstance(self.dfTemp, str):
                    messagebox.showerror(message=self.dfTemp)
                else:
                    self.df = self.dfTemp
                    guiFunctions.showData(self.df,
                        self.previewLabel2, self.shapeLabel2,
                        buttonToChange=self.saveButton)
                    guiFunctions.refreshLists(self.df,
                        [self.manualListBox])

                    list = [{'widget': self.manualTextBox, 'type': 'textbox'},
                            {'widget': self.manualBinsEntry, 'type': 'entry', 'special': False}]
                    guiFunctions.emptyWidgets(list)
                    guiFunctions.showHideFrames([self.manualFrame])
                    guiFunctions.disableWidget(self.clusterButton,
                        'button')
                    self.dropClVar.set('')
            else:
                messagebox.showerror(message='Missing the number of bins to create.')
        except IndexError as ie:
            messagebox.showerror(message='Select a column to cluster on!\n"%s"' % ie)
        except TypeError:
            messagebox.showerror(message="Can't cluster on postcode. "
                "Select a column containing numbers.")
# ******************************************************************************
    def triggerLoadingData(self):
        self.df = guiFunctions.loadingData(self.pathEntry, self.typeVar,
            'clustering', listboxes=[self.manualListBox],
            previewLabel=self.previewLabel2, shapeLabel=self.shapeLabel2,
            saveButton=self.saveButton)
