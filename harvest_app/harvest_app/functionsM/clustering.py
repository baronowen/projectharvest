import numpy as np
import pandas as pd

def clusterManual(dfName, toCluster, nBins, labelList):
    """
    Clusters the dataframe on the column in toCluster.
    The number of bins to create is provided in the nBins parameter.
    """
    temp = dfName.loc[:]
    if labelList:
        label = 'bin'
        if len(labelList) == int(nBins):
            temp[label] = pd.cut(temp[toCluster], nBins, labels=labelList)
            temp[label] = temp[label].astype('category')
            temp['cat'] = temp[label].cat.codes
            return temp
        else:
            return 'Number of labels do not match the number of Bins specified!'
    else:
        return 'No labels given!'
