import tkinter as tk
from tkinter import messagebox
import pandas as pd
import sys
sys.path.append('../')

from harvest_app.functionsM import apiFunctions, extraFunctions, guiFunctions

class AdwordsPage(tk.Frame):
    """
    The page for interacting with the AdWords API.
    """
    padx=5
    pady=5

    color = "#FF8000"
    color2 = "#1CC2E5"
    df = pd.DataFrame()
    dfTemp = pd.DataFrame()
    percenDict = None
    selectedCampaign = None

    rows = 0
    cols = 1
    rowsDisp = 5
    colsDisp = 1

    def __init__(self, parent, controller):
        """Initialize the page, creates all widgets."""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, fg='white', bg='black',
            text='Google AdWords page')
        label.grid(column=0, row=0, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
        navFrame = tk.Frame(self, bg=self.color, bd=10)
        navFrame.grid(column=0, row=1, columnspan=2, sticky='WE')

        buttonDLC = tk.Button(navFrame,
            text="Go to Data Loading and Cleaning page",
            command=lambda: controller.show_frame("DataLCPage"))
        buttonDLC.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        buttonM = tk.Button(navFrame, text="Go to Merge page",
            command=lambda: controller.show_frame("MergePage"))
        buttonM.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        buttonManip = tk.Button(navFrame, text="Go to Data Manipulation page",
            command=lambda: controller.show_frame("DataManipPage"))
        buttonManip.grid(column=2, row=0, padx=self.padx, pady=self.pady)

        buttonCluster = tk.Button(navFrame, text="Go to Cluster page",
            command=lambda: controller.show_frame("ClusteringPage"))
        buttonCluster.grid(column=3, row=0, padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
        self.leftFrame = tk.Frame(self, bg=self.color, bd=10)
        self.leftFrame.grid(column=0, row=3, sticky='NS')

        self.rightFrame = tk.Frame(self, bg=self.color, bd=10)
        self.rightFrame.grid(column=1, row=3, sticky='NS')

        self.clearButton = tk.Button(self,
            text="Clear all entry fields, text boxes, labels etc",
            command=self.callEmptyWidgets)
        self.clearButton.grid(column=0, row=2, columnspan=2,
            padx=self.padx, pady=self.pady)

        self.widgets()
        # Retrieve info from config.txt.
        cDict = extraFunctions.retrieveFromConfig()
        if isinstance(cDict, str):
            print(cDict)
        else:
        # Update client ID with ID to use from config.txt.
            extraFunctions.updateClientId(cDict['idToUse'])
        # Call API to load accounts.
        self.callLoadAccounts(self.gaListBox)

    def widgets(self):
        """
        Creat the widgets for loading the data, viewing the data and interacting
        with the API.
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
# PreviewFrame------------------------------------------------------------------------------
        previewFrame = tk.Frame(self.leftFrame, bg=self.color2, bd=10)
        previewFrame.grid(column=0, row=1, sticky='N')

        self.previewLabel2 = tk.Label(previewFrame)
        self.previewLabel2.grid(column=0, row=1,
            padx=self.padx, pady=self.pady)

        shapeLabel = tk.Label(previewFrame, text='Shape of the data (rows, columns)')
        shapeLabel.grid(column=0, row=2,
            padx=self.padx, pady=self.pady)

        self.shapeLabel2 = tk.Label(previewFrame)
        self.shapeLabel2.grid(column=0, row=3,
            padx=self.padx, pady=self.pady)
# GAFrame------------------------------------------------------------------------------
        gaFrame = tk.Frame(self.rightFrame, bg=self.color2, bd=10)
        gaFrame.grid(column=0, row=0)

        self.selectFrame = tk.Frame(gaFrame, bg=self.color2, bd=10)
        self.selectFrame.grid(column=0, row=0)

        self.backButton = tk.Button(self.selectFrame, text="Go back")
        self.backButton.grid(column=0, row=0, sticky='W')
        self.backButton.grid_remove()

        self.gaLabel = tk.Label(self.selectFrame, text="Accounts under manager:")
        self.gaLabel.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        self.refreshButton = tk.Button(self.selectFrame, text='Refresh accounts',
            command=self.refreshAccounts)
        self.refreshButton.grid(column=2, row=0, sticky='E')

        self.gaListBox = tk.Listbox(self.selectFrame, exportselection=0,
            height=10, width=40)
        self.gaListBox.grid(column=1, row=1, padx=self.padx, pady=self.pady)

        self.nothingFoundLabel = tk.Label(self.selectFrame,
            text="No campaigns were found.")
        self.nothingFoundLabel.grid(column=1, row=1, padx=self.padx, pady=self.pady)
        self.nothingFoundLabel.grid_remove()

        self.loadButton = tk.Button(self.selectFrame, text="Load all campaigns.",
            command=lambda: self.callLoadCampaigns(self.gaListBox))
        self.loadButton.grid(column=1, row=2, padx=self.padx, pady=self.pady)
# ******************************************************************************
        self.campaignInfo = tk.Label(self.selectFrame, text='Campaign info:')
        self.campaignInfo.grid(column=1, row=1, sticky='S',
            padx=self.padx, pady=self.pady)
        self.campaignInfo.grid_remove()

        self.campaignInfo2 = tk.Label(self.selectFrame, text='test')
        self.campaignInfo2.grid(column=1, row=2, sticky='N',
            padx=self.padx, pady=self.pady)
        self.campaignInfo2.grid_remove()

        self.targetingInfo = tk.Label(self.selectFrame,
            text='Postcodes currently being targeted\nand their bid modifier:')
        self.targetingInfo.grid(column=2, row=1, padx=self.padx, pady=self.pady)
        self.targetingInfo.grid_remove()

        self.targetingFrame = tk.Frame(self.selectFrame, bd=0)
        self.targetingFrame.grid(column=2, row=2)
        self.targetingFrame.grid_remove()

        self.canvas = tk.Canvas(self.targetingFrame)
        self.canvas.grid(column=0, row=0)

        vsbar = tk.Scrollbar(self.targetingFrame, orient='vertical',
            command=self.canvas.yview)
        vsbar.grid(column=1, row=0, sticky='NS')
        self.canvas.configure(yscrollcommand=vsbar.set)

        self.targetFrame = tk.Frame(self.canvas, bd=0)
# ******************************************************************************
        self.mutateFrame = tk.Frame(gaFrame, bg=self.color2, bd=10)
        self.mutateFrame.grid(column=0, row=1)
        self.mutateFrame.grid_remove()

        mutateLabel = tk.Label(self.mutateFrame, text='Postcode\tbid modifier')
        mutateLabel.grid(column=0, row=0, columnspan=2, sticky='S',
            padx=self.padx, pady=self.pady)

        self.mutateListBox = tk.Listbox(self.mutateFrame, exportselection=0,
            height=5, width=25, selectmode='multiple')
        self.mutateListBox.grid(column=0, row=1, rowspan=2, columnspan=2,
            padx=self.padx, pady=self.pady)

        removeButton = tk.Button(self.mutateFrame,
            text="Remove selected postcode(s)",
            command=lambda: self.callRemoveCampaignCriteria(self.mutateListBox))
        removeButton.grid(column=0, row=3, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)

        newPostcodeLabel = tk.Label(self.mutateFrame, text='New postcode:')
        newPostcodeLabel.grid(column=0, row=4, padx=self.padx, pady=self.pady)

        vcmd = (self.register(self.validateNewPostcode), '%S')

        self.newPostcodeEntry = tk.Entry(self.mutateFrame, width=10,
            validate='key', validatecommand=vcmd)
        self.newPostcodeEntry.grid(column=1, row=4,
            padx=self.padx, pady=self.pady)

        addPostcodeButton = tk.Button(self.mutateFrame,
            text="Add new targeting postcode",
            command=lambda: self.callAddCampaignCriteria(self.newPostcodeEntry))
        addPostcodeButton.grid(column=0, row=5, columnspan=2, sticky='WE',
            padx=self.padx, pady=self.pady)

        updateLabel = tk.Label(self.mutateFrame,
            text="Update bid modifier manually percentage.\n\n"
                "Type a whole percentages between -90 and 900.\n"
                "Percentages like 25.5 are not supported!")
        updateLabel.grid(column=2, row=0, columnspan=3, sticky='WE',
            padx=self.padx, pady=self.pady)

        bidModLabel = tk.Label(self.mutateFrame, text='New bid modifier:')
        bidModLabel.grid(column=2, row=1, sticky='E',
            padx=self.padx, pady=self.pady)

        vcmd2 = (self.register(self.validateBidMod), '%S')

        self.bidModEntry = tk.Entry(self.mutateFrame, width=5,
            validate='key', validatecommand=vcmd2)
        self.bidModEntry.grid(column=3, row=1, padx=self.padx, pady=self.pady)

        percenLabel = tk.Label(self.mutateFrame, text='%')
        percenLabel.grid(column=4, row=1, sticky='W',
            padx=self.padx, pady=self.pady)

        updateButton = tk.Button(self.mutateFrame, text='Update bid modifier',
            command=lambda: self.callUpdateCampaignCriteria(self.mutateListBox))
        updateButton.grid(column=2, row=2, columnspan=3, sticky='WE',
            padx=self.padx, pady=self.pady)

        autoTargetButton = tk.Button(self.mutateFrame,
            text='Auto target best categories.',
            command=self.autoTarget)
        autoTargetButton.grid(column=2, row=4, rowspan=2, columnspan=3,
            sticky='NSWE', padx=self.padx, pady=self.pady)
# ------------------------------------------------------------------------------
    def callEmptyWidgets(self):
        self.df = pd.DataFrame()
        self.dfTemp = pd.DataFrame()
        percenDict = None
        guiFunctions.emptyWidgets(
            [{'widget': self.previewLabel2, 'type': 'label'},
            {'widget': self.shapeLabel2, 'type': 'label'},
            {'widget': self.pathEntry, 'type': 'entry', 'special': True},
            {'widget': self.newPostcodeEntry, 'type': 'entry', 'special': False},
            {'widget': self.bidModEntry, 'type': 'entry', 'special': False}])

    def validateBidMod(self, S):
        """Only allow numbers and a dash to be typed."""
        if S in '0123456789-':
            return True
        else:
            self.bell()
            return False

    def validateNewPostcode(self, S):
        """Only allow upper case to be typed."""
        if S == S.upper() and S not in '!@#$%^&*()_+-=€[]{};":,./<>?`~':
            return True
        else:
            self.bell()
            return False

    def callLoadAccounts(self, listBox):
        """Function to call API to retrieve accounts."""
        accountList = apiFunctions.loadAccounts()
        id = extraFunctions.retrieveClientId()
        if isinstance(accountList, str):
            listBox.delete(0, 'end')
            warning = '%s "%s".' %(accountList, id)
            messagebox.showerror(message=warning)
        else:
            listBox.delete(0, 'end')
            i = 0
            for account in accountList:
                if id == account['customerId']:
                    i += 1
                else:
                    i += 1
                    # Update list box to show the accounts.
                    listBox.insert(i, '%s, %s' % (account['name'], account['customerId']))

    def callLoadCampaigns(self, listBox):
        """Function that calls API to get all campaigns."""
        item = guiFunctions.retrieveItems(listBox, 'listBox')
        if not item:
            messagebox.showerror(message='Select an account from the list box!')
        else:
            for x in item:
                name = x.split(', ')[0]
                id = x.split(', ')[1]
            # Update client ID in googleads.yaml.
            extraFunctions.updateClientId(id)
            campaignList = apiFunctions.loadCampaigns()
            listBox.delete(0, 'end')
            i = 0
            # Check if campaigns are found.
            if not campaignList:
                guiFunctions.showHideFrames([self.gaListBox, self.loadButton,
                    self.refreshButton], [self.nothingFoundLabel, self.backButton])
                self.loadButton.configure(state='disabled')
                self.backButton.configure(command=lambda: self.backToManager())
                self.gaLabel.configure(text="Campaigns under account: '%s'." % name)
            else:
                for campaign in campaignList:
                    i += 1
                    listBox.insert(i, '%s, %s' % (campaign['name'], campaign['id']))
                guiFunctions.showHideFrames([self.refreshButton], [self.backButton])
                self.backButton.configure(command=lambda: self.backToManager())
                self.gaLabel.configure(text="Campaigns under account: '%s'." % name)
                self.loadButton.configure(text='Retrieve campaign information.',
                    command=lambda: self.callLoad1Campaign(self.gaListBox))

    def callLoad1Campaign(self, listBox):
        """Function that loads information from 1 specific campaign."""
        item = guiFunctions.retrieveItems(listBox, 'listBox')
        # Check if an item is selected.
        if not item:
            messagebox.showerror(message='Select a campaign from the list box!')
        else:
            for x in item:
                name = x.split(', ')[0]
                id = x.split(', ')[1]
            self.selectedCampaign = id
            self.backButton.configure(command=lambda: self.backToCampaigns())
            # Call updateWidgets, which also retrieves the information.
            self.updateWidgets(self.campaignInfo2, self.mutateListBox)
            guiFunctions.showHideFrames([self.gaLabel, self.gaListBox,
                self.loadButton], [self.campaignInfo, self.campaignInfo2,
                self.targetingInfo, self.targetingFrame, self.mutateFrame])

    def callAddCampaignCriteria(self, postcodeEntry):
        """"Function that adds a location criteria to a campaign."""
        postcode = postcodeEntry.get()
        id = self.selectedCampaign
        postcodes = self.getCurrentTargets(self.targetFrame)
        if postcode:
            # Call add function
            message = apiFunctions.addCampaignCriteria(id, [postcode],
                postcodes)
            if message:
                messagebox.showerror(message=message)
            else:
                # Call updateWidgets to retrieve the new information.
                self.updateWidgets(self.campaignInfo2, self.mutateListBox)
        else:
            messagebox.showerror(message='Type the postcode you wish to add!')

    def callRemoveCampaignCriteria(self, listBox):
        """Function that removes a location criteria from a campaign."""
        items = guiFunctions.retrieveItems(listBox, 'listBox')
        id = self.selectedCampaign
        postcodes = self.getCurrentTargets(self.targetFrame)
        postcodesToRemove = []
        # Check if locations are selected.
        if not items:
            messagebox.showerror(message='Select one or more postcodes to remove!')
        else:
            for item in items:
                item = item.split()[0]
                postcodesToRemove.append(item)
            # Call remove function.
            message = apiFunctions.removeCampaignCriteria(id,
                postcodesToRemove, postcodes)
            if message:
                messagebox.showerror(message=message)
            else:
                self.updateWidgets(self.campaignInfo2, listBox)

    def callUpdateCampaignCriteria(self, listBox):
        """
        Function that updates the bid modifier of a location criteria.

        To update a location criteria, you first need to check if there are changes,
        and if there are, remove the old and add the new.
        """
        id = self.selectedCampaign
        toUpdate = []
        bidMod = self.bidModEntry.get()
        if not bidMod:
            messagebox.showerror(message='No value given for bid modifier percentage!')
        else:
            bidMod = int(bidMod)
            min = -90
            max = 900
            # Check wether bidMod is between min/max values to prevent API error.
            if bidMod < min:
                messagebox.showerror(message='Bid modifier too small.')
            elif bidMod > max:
                messagebox.showerror(message='Bid modifier too big.')
            else:
                bidMod = (bidMod + 100) / 100
                items = guiFunctions.retrieveItems(listBox, 'listBox')
                # Check if something is selected.
                if not items:
                    messagebox.showerror(message='Select one or more postcodes to update.')
                else:
                    for item in items:
                        postcode = item.split()[0]
                        toUpdate.append(postcode)
                    # Retrieves postcodes that are being targeted.
                    currentTargets = self.getCurrentTargets(self.targetFrame)
                    # Call update function.
                    message = apiFunctions.updateCampaignCriteria(id, toUpdate,
                        currentTargets, bidMod)
                    if message:
                        messagebox.showerror(message=message)
                    else:
                        self.updateWidgets(self.campaignInfo2, listBox)
                        guiFunctions.emptyWidgets([
                            {'widget': self.bidModEntry, 'type': 'entry', 'special': False}
                        ])

    def autoTarget(self):
        """
        Targets the postcodes in the best categories with
        the assigned bid modifier percentage.
        """
        print()
        addList = []
        updateList = []
        operations = []
        cDict = extraFunctions.retrieveFromConfig()
        if isinstance(cDict, str):
            messagebox.showerror(message=cDict)
        else:
            if self.df.empty:
                messagebox.showerror(message='No data loaded in!')
            else:
                result = messagebox.askquestion(message='Using %s as '
                    'minimum and %s as maximum for '
                    'assinging bid modifier percentages.\nDo you wish to continue?' %
                    (cDict['min'], cDict['max']))
                if result == 'no':
                    pass
                elif result == 'yes':
                    # Running assignBidMod function.
                    temp = extraFunctions.assignBidMod(self.df, cDict['min'], cDict['max'])
                    if isinstance(temp, str):
                        messagebox.showerror(message=temp)
                    else:
                        self.percenDict = temp
                        # Create a list of the keys.
                        catList = list(self.percenDict.keys())
                        # Grabbing the last two list entries.
                        catListSmall = catList[-2:]
                        id = self.selectedCampaign
                        # Retrieve current targets.
                        currentTargets = self.getCurrentTargets(self.targetFrame)
                        # Looping over categories in the smaller list.
                        for cat in catListSmall:
                            bidMod = self.percenDict[cat]
                            # Convert bidMod to correct format.
                            bidMod = (bidMod+100)/100
                            temp = self.df.loc[self.df['bin'] == cat]
                            temp = list(temp['postcode'])
                            # Loop over postcode in temp
                            for postcode in temp:
                                # Check if postcode is in current targets.
                                if postcode in currentTargets:
                                    updateList.append(postcode)
                                else:
                                    addList.append(postcode)
                            # Check for entries in addList
                            if addList:
                                # Call API to add
                                opsAdd = apiFunctions.addCampaignCriteria(id,
                                    addList, currentTargets, bidMod, returnOp=True)
                                if isinstance(opsAdd, str):
                                    pass
                                else:
                                    # Add add operations to list
                                    for op in opsAdd:
                                        operations.append(op)
                            else:
                                pass
                            # Check for entries in updateList
                            if updateList:
                                # Call API to update
                                opsUpdate = apiFunctions.updateCampaignCriteria(id,
                                    updateList, currentTargets, bidMod, returnOp=True)
                                if isinstance(opsUpdate, str):
                                    pass
                                else:
                                    # Add update operations to the same list as before.
                                    for op in opsUpdate:
                                        operations.append(op)
                            else:
                                pass
                            # Empty addList and updateList
                            addList.clear()
                            updateList.clear()
                        if operations:
                            # Call function that sends 1 mutate call.
                            message = apiFunctions.callCampCritApi(operations)
                            if message:
                                pass
                            else:
                                # Update the widgets.
                                self.updateWidgets(self.campaignInfo2, self.mutateListBox)
                        else:
                            messagebox.showinfo(message='All targeted postcodes '
                                'already have the right bid modifier percentage.')
                else:
                    pass

    def refreshAccounts(self):
        """
        Refreshes the account list by reading the config.txt file and calling API.
        API call for accounts now catches exception.
        """
        currentId = extraFunctions.retrieveClientId()
        cDict = extraFunctions.retrieveFromConfig()
        if isinstance(cDict, dict):
            id = cDict['idToUse']
            if id.isdigit():
                if id == currentId:
                    messagebox.showerror(message='ID to use "%s" is the '
                    'same as the current ID "%s".' % (id, currentId))
                else:
                    extraFunctions.updateClientId(id)
                    self.callLoadAccounts(self.gaListBox)
            else:
                messagebox.showerror(message='ID to use has to be numbers '
                'only!\n"%s" is not numbers only!' % id)
        else:
            messagebox.showerror(message=cDict)

    def backToManager(self):
        """Function to go back to all accounts under the manager."""
        self.selectedCampaign = None
        guiFunctions.showHideFrames([self.backButton, self.nothingFoundLabel],
            [self.gaListBox, self.loadButton, self.refreshButton])
        managerId = extraFunctions.retrieveFromConfig()['idToUse']
        extraFunctions.updateClientId(managerId)
        self.callLoadAccounts(self.gaListBox)
        self.gaLabel.configure(text='Accounts under manager:')
        self.loadButton.configure(text='Load all campaigns.',
            command=lambda: self.callLoadCampaigns(self.gaListBox),
            state='normal')

    def backToCampaigns(self):
        """Function to go back to all campaigns from 1 campaign."""
        self.selectedCampaign = None
        guiFunctions.emptyWidgets(
            [{'widget': self.campaignInfo2, 'type': 'label'},
            {'widget': self.mutateListBox, 'type': 'listbox'},
            {'widget': self.newPostcodeEntry, 'type': 'entry', 'special': False},
            {'widget': self.bidModEntry, 'type': 'entry', 'special': False}])
        widgets = self.targetFrame.winfo_children()
        for child in widgets:
            child.destroy()
        guiFunctions.showHideFrames([self.campaignInfo,
            self.campaignInfo2, self.targetingInfo, self.targetingFrame,
            self.mutateFrame], [self.gaLabel, self.gaListBox,
            self.loadButton])
        self.backButton.configure(command=lambda: self.backToManager())

    def updateWidgets(self, campaignLabel, listBox):
        """
        Function that retrieves current campaign information,
        and updates the widgets to show that information.
        """
        id = self.selectedCampaign
        campaign = apiFunctions.load1Campaign(id)
        dictWithBid = apiFunctions.loadCampaignCriteriaWithBid(id)
        # Set the text for the campaignLabel.
        campaignLabel.configure(text=
            'ID:\t%s\n'
            'Name:\t%s\nStart date:\t%s\nEnd date: \t%s\n'
            'Status:\t%s\nBudget:\t£%s'
            % (campaign['id'], campaign['name'], campaign['startDate'],
            campaign['endDate'], campaign['status'],
            campaign['budget']['amount']['microAmount']/1000000))
        # Empty list box.
        listBox.delete(0, 'end')

        children = self.targetFrame.winfo_children()
        if children:
            self.targetFrame.destroy()
            self.targetFrame = tk.Frame(self.canvas, bd=0)
        else:
            pass
        l2 = []
        i = 1
        # Creating the window for targetFrame.
        self.canvas.create_window((0,0), window=self.targetFrame, anchor='nw')
        if dictWithBid:
            # Looping over dict to add to label and to calculate bid modifier percentage.
            for info in dictWithBid:
                bidMod = info['bidMod']
                # Check if bidMod is None.
                if bidMod == None:
                    bidMod = 0
                else:
                    # Calculate the percentage.
                    bidMod = round((bidMod * 100) - 100)
                # Creating strings to add to label and list box.
                string = '%s        %s%%' % (info['name'], bidMod)
                l2.append('%s       %s%% \n' % (info['name'], bidMod))
                # Add label with string as text to frame within canvas.
                temp = tk.Label(self.targetFrame, padx=5, pady=1,
                    text=string)
                temp.grid(column=0, row=i, sticky='news')
                i += 1
            # Adding rows to list box.
            i = 0
            for set in l2:
                i += 1
                listBox.insert(i, set)
            # Getting number of rows.
            self.rows = len(dictWithBid)
            # Creating the window for targetFrame.
            self.canvas.create_window((0,0), window=self.targetFrame, anchor='nw')
            # Enable bbox?
            self.targetFrame.update_idletasks()
            bbox = self.canvas.bbox(tk.ALL)
            # Setting the size of the canvas and scrollbar
            # Determining the full width and height of the canvas
            w, h = bbox[2]-bbox[1], bbox[3] - bbox[1]
            # Setting the display width and height of the canvas
            # dw, dh = int((w/self.cols) * self.colsDisp), int((h/self.rows) * self.rowsDisp)
            dw, dh = 86, 105
            self.canvas.configure(scrollregion=bbox, width=dw, height=dh)
        else:
            # messagebox.showinfo(message='No location criteria for this campaign.')
            self.canvas.create_window((0,0), window=self.targetFrame, anchor='nw')
            # self.targetFrame.update_idletasks()
            bbox = self.canvas.bbox(tk.ALL)
            dw, dh = 86, 105
            self.canvas.configure(scrollregion=bbox, width=dw, height=dh)

    def getCurrentTargets(self, targetFrame):
        """Function that retrieves the currently targeted location criteria."""
        # Retrieve all children of targetFrame.
        widgets = targetFrame.winfo_children()
        list2 = []
        postcodes = []
        # Loop over children and retrieve the text.
        for w in widgets:
            text = w['text']
            list2.append(text)
        # Loop over list with the text and split it.
        for widget in list2:
            postcode = widget.split()[0]
            postcodes.append(postcode)
        return postcodes
# ------------------------------------------------------------------------------
    def triggerLoadingData(self):
        self.df = guiFunctions.loadingData(self.pathEntry, self.typeVar,
            'adwords', previewLabel=self.previewLabel2,
            shapeLabel=self.shapeLabel2)
