import pandas as pd
import numpy as np

def updateClientId(clientId, fileName='data/config file API/googleads.yaml', rowNumber=10):
    """
    This function works when ran by pressing 'f5'.
    A file not found error will be thrown when ran by using 'ctrl + shift + b'.
    """
    with open(fileName, 'r') as f:
        get_all=f.readlines()
    with open(fileName, 'w') as f:
        for i , line in enumerate(get_all, 1):
            # Change the client id on the specified row number.
            if i == rowNumber:
                if clientId:
                    f.writelines("  client_customer_id: '%s'\n" % clientId)
                else:
                    f.writelines("  # client_customer_id: INSERT_CLIENT_CUSTOMER_ID_HERE\n")
            else:
                f.writelines(line)

def retrieveFromConfig(filename='data/config file API/config.txt'):
    """
    Retrieves information from the config.txt file and puts it
    all in a dictionary that is returned.
    """
    try:
        with open(filename, 'r') as f:
            get_all = f.readlines()
            configDict = {}
            for i, line in enumerate(get_all, 1):
                str1 = line.split(':')[0].strip()
                if str1 == 'client_ID_to_use':
                    l = []
                    str2 = line.split(':')[1].strip()
                    for char in str2:
                        if char == "'" or char == '"':
                            pass
                        else:
                            l.append(char)
                    id = ''.join(l)
                    configDict['idToUse'] = id
                elif str1 == 'min_percen':
                    str2 = line.split(':')[1].strip()
                    str2 = int(str2)
                    configDict['min'] = str2
                elif str1 == 'max_percen':
                    str2 = line.split(':')[1].strip()
                    str2 = int(str2)
                    configDict['max'] = str2
                else:
                    pass
        return configDict
    except ValueError as error:
        return 'Found letters instead of numbers when looking for min and max in config.txt.'
    except FileNotFoundError as error:
        return 'Could not find file "%s".\nError message: %s' % (filename, error)

def retrieveClientId(fileName='data/config file API/googleads.yaml', rowNumber=10):
    """
    This function retrieves the current client customer id from
    the googleads.yaml file. It is used to prevent the manager account
    from showing in the list box with all the other accounts.
    """
    # Open file for reading.
    with open(fileName, 'r') as f:
        get_all = f.readlines()
        # Loop over the lines.
        for i, line in enumerate(get_all, 1):
            # Check for row number.
            if i == rowNumber:
                string = line
    # Split on ': '.
    string = string.split(': ')[1]
    string = string.strip()
    l = []
    # Looping over each char in the string to remove "'".
    for char in string:
        if char == "'":
            pass
        else:
            l.append(char)
    # Joining the string back together.
    id = ''.join(l)
    return id

def assignBidMod(dfName, lowPercen, highPercen):
    """
    This function assigns a bid modifier percentage to the categories
    inside a dataframe.
    """
    # Creating empty lists.
    rangeList = []
    lists = []
    percenList = []
    # Counting how many times each bin occures.
    if 'bin' in dfName.columns:
        temp = dfName['bin'].value_counts()
        # Convert to dictionary.
        tempDict = temp.to_dict()
        # Setting the number bins.
        bins = len(tempDict)
        # Creating a list of dictionary keys.
        catList = list(tempDict.keys())
        # Filling rangeList.
        for i in range(lowPercen, highPercen):
            rangeList.append(i)
        # Retrieving the lenght of this list.
        length = len(rangeList)
        # Calculating the size of each bin.
        binSize = round(length/bins)

        i = 0
        start = 0
        stop = binSize
        # Start while loop.
        while i < bins:
            temp = rangeList[start : stop]
            lists.append(temp)
            start = stop
            stop += binSize
            i += 1
        # Looping over lists and calculating the mean of each sub list
        for cat in lists:
            temp = round(np.mean(cat))
            temp = int(temp)
            percenList.append(temp)
        # Combining catList and percenList into a dictionary.
        percenDict = dict(zip(catList, percenList))
        return percenDict
    else:
        return 'Missing a category column in dataframe!'
