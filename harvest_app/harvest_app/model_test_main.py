# import numpy as np
# import pandas as pd

# from functionsM.dataLoading import *
# from functionsM.data_cleaning import *
# from functionsM.clustering import *
# from functionsM.dataManipFunctions import *

# data = loadData("../data/convHNew.csv", 'csv')
# print(data.head(), '\nShape after loading in: ', data.shape, '\n')
#
# data2 = loadData("../data/healthv2.csv", 'csv')
# print(data2.head(), '\n')
#
# test = extractConv(data, data2, 'Price_agreed', 'postcode')
# print(test.head(), '\n')

# calcPercen(data, ['Very good health', 'Good health', 'Fair health', 'Bad health'])

# test = [{'Widget':'manualTextBox', 'Type': 'textBox'},
#         {'Widget':'manualBinsEntry', 'Type': 'entry'}]
#
# for d in test:
#     print(d["Widget"])
