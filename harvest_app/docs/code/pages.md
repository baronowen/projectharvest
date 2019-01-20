# Package Pages
This package contains all the pages of the GUI, and this document will contain a list of all functions and where to find them.

## AdWordsPage
Page for interacting with the Google AdWords API.
Function | File | Row number
--- | --- | ---
`__init__()`                   | `guiAdwords.py` | 28
`widgets()`                    | `guiAdwords.py` | 77
`callEmptyWidgets()`           | `guiAdwords.py` | 264
`validateBidMod()`             | `guiAdwords.py` | 275
`validateNewPostcode()`        | `guiAdwords.py` | 283
`callLoadAccounts()`           | `guiAdwords.py` | 291
`callLoadCampaigns()`          | `guiAdwords.py` | 310
`callLoad1Campaign()`          | `guiAdwords.py` | 341
`callAddCampaignCriteria()`    | `guiAdwords.py` | 359
`callRemoveCampaignCriteria()` | `guiAdwords.py` | 376
`callUpdateCampaignCriteria()` | `guiAdwords.py` | 397
`autoTarget()`                 | `guiAdwords.py` | 441
`refreshAccounts()`            | `guiAdWords.py` | 521
`backToManager()`              | `guiAdwords.py` | 538
`backToCampaigns()`            | `guiAdwords.py` | 551
`updateWidgets()`              | `guiAdwords.py` | 568
`getCurrentTargets()`          | `guiAdwords.py` | 642
`triggerLoadingData()`         | `guiAdwords.py` | 658

## ClusteringPage
Page for clustering data.
Function | File | Row number
--- | --- | ---
`__init__()`           | `guiCluster.py` | 28
`callEmptyWidgets()`   | `guiCluster.py` | 209
`validateBins()`       | `guiCluster.py` | 223
`changeDropCluster()`  | `guiCluster.py` | 231
`noChoiceMadeCl()`     | `guiCluster.py` | 243
`choseManual()`        | `guiCluster.py` | 248
`execManual()`         | `guiCluster.py` | 255
`triggerLoadingData()` | `guiCluster.py` | 293

## DataLCPage
Page for data loading and cleaning.

Function | File | Row Number
---|---|---
`__init__()`             | `guiDataLC.py` | 32
`widgets()`              | `guiDataLC.py` | 77
`callEmptyWidgets()`     | `guiDataLC.py` | 235
`changeDropC()`          | `guiDataLC.py` | 250
`noChoiceMade()`         | `guiDataLC.py` | 273
`choseDrop1()`           | `guiDataLC.py` | 281
`execDrop1()`            | `guiDataLC.py` | 296
`choseDrop2()`           | `guiDataLC.py` | 323
`execDrop2()`            | `guiDataLC.py` | 336
`choseCopyAndDrop()`     | `guiDataLC.py` | 362
`execCopyAndDrop()`      | `guiDataLC.py` | 375
`choseFill()`            | `guiDataLC.py` | 406
`execFill()`             | `guiDataLC.py` | 419
`choseString()`          | `guiDataLC.py` | 446
`execString()`           | `guiDataLC.py` | 459
`choseRename()`          | `guiDataLC.py` | 478
`execRename()`           | `guiDataLC.py` | 491
`choseRemoveW()`         | `guiDataLC.py` | 516
`choseShortenPostcode()` | `guiDataLC.py` | 548
`execShortenPostcode()`  | `guiDataLC.py` | 560
`triggerLoadingData()`   | `guiDataLC.py` | 583

## DataManipPage
Page for data manipulation.
Function | File | Row Number
---|---|---
`__init__()`           | `guiDataManip.py` | 33
`widgets()`            | `guiDataManip.py` | 77
`callEmptyWidgets()`   | `guiDataManip.py` | 192
`changeDropManip()`    | `guiDataManip.py` | 205
`noChoiceMadeManip()`  | `guiDataManip.py` | 218
`choseExtract()`       | `guiDataManip.py` | 225
`execExtract()`        | `guiDataManip.py` | 236
`choseEncode()`        | `guiDataManip.py` | 258
`execEncode()`         | `guiDataManip.py` | 269
`choseCalculate()`     | `guiDataManip.py` | 291
`execCalculate()`      | `guiDataManip.py` | 303
`triggerLoadingData()` | `guiDataManip.py` | 322

## MergePage
Page for merging two datasets.
Function | File | Row Number
---|---|---
`__init__()`           | `guiMerging.py` | 19
`widgets()`            | `guiMerging.py` | 60
`callEmptyWidgets()`   | `guiMerging.py` | 195
`triggerLoadingData()` | `guiMerging.py` | 208
`merge()`              | `guiMerging.py` | 218
