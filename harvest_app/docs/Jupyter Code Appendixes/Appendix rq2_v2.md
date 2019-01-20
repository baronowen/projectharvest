# Code appendix RQ2
The code appendix for notebook `Data_analyses_rq2_v2`.
The code in this appendix will appear in the same order as in the notebook.

## Loading data
```python
convA = pd.read_csv('../harvestApp/Model/data/convA.csv')

labelEncoder = LabelEncoder()
labelEncoder.fit(convA['postcode'])
convA['postcode1'] = labelEncoder.transform(convA['postcode'])

convACopy = convA[['postcode', 'postcode1', 'latitude', 'longitude']]
convA.drop(['postcode', 'latitude', 'longitude'], axis=1, inplace=True)

# convA['difference'] = convA['total'] - convA['# converted']

convA.head()
```

## Manual
<b><u>Using manual and plotting</u></b>
```python
# Manual on column 'difference'
clusteredM = cutDataFrame(convA, 'difference', 4,
    'bad', 'decent', 'good', 'very good')
clusteredM.head()

# Plotting outcome
print(convA.shape)
plt.figure('manul', figsize=(10,5))
plt.scatter(clusteredM['total'], clusteredM['difference'],
    c=clusteredM['cat'], cmap='viridis')
plt.xlabel('total people that can be converted')
plt.ylabel('total people left to be converted')
plt.show()

# Manual on column '45 to 64'
clusteredM2 = cutDataFrame(convA, '45 to 64', 4,
    'bad', 'decent', 'good', 'very good')
clusteredM2.head()

# Plotting the outcome
print(clusteredM2.shape)
plt.figure('manual2', figsize=(10,5))
plt.scatter(clusteredM2['total residents'],
    clusteredM2['45 to 64'], alpha=0.8, c=clusteredM2['cat'], cmap='viridis')
plt.xlabel('total people')
plt.ylabel('total people between 45 and 64')
plt.show()
```

## K-Means
<b><u>K-Means on 1 column</u></b>
```python
y = convA[['difference']]
x = convA[['total']]

# Elbow curve
nc = range(1,15)
kmeans = [KMeans(n_clusters=i) for i in nc]
kmeans
score = [kmeans[i].fit(y).score(y) for i in range(len(kmeans))]
score
plt.plot(nc, score)
plt.xlabel('number of cluster')
plt.ylabel('score')
plt.title('elbow curve')
plt.show()

# Converting to set of linear combinations
pca = PCA(n_components=1).fit(y)
pca_y = pca.transform(y)
pca_x = pca.transform(x)

# Reference plot.
plt.subplot(121)
# plt.figure('reference')
plt.scatter(convA['total'], convA['difference'])
plt.ylabel('difference')
plt.xlabel('total')

# Clustering.
kmeans = KMeans(n_clusters=4, random_state=0)
kmeansOutput = kmeans.fit(y)
kmeansOutput

# Cluster plot.
plt.subplot(122)
# plt.figure('4 cluster kmeans')
plt.scatter(pca_x[:,0], pca_y[:,0], alpha=1, c=kmeansOutput.labels_, cmap='viridis')
plt.ylabel('difference')
plt.xlabel('total')
plt.show()
```
<b><u>K-Means on entire dataframe</u></b>
```python
Converting to set of linear combinations
pca2 = PCA(n_components=2).fit(convA)
pca2 = pca2.transform(convA)

# Elbow curve
nc = range(1,15)
kmeans = [KMeans(n_clusters=i) for i in nc]
kmeans
score = [kmeans[i].fit(y).score(y) for i in range(len(kmeans))]
score
plt.plot(nc, score)
plt.show()

# Reference plot.
plt.subplot(121)
# plt.figure('reference plot')
plt.scatter(pca2[:,0], pca2[:,1])

# Clustering.
kmeans = KMeans(n_clusters=4, random_state=111)
kmeans.fit(convA)

# Cluster plot
plt.subplot(122)
# plt.figure('kmeans with 4 clusters')
plt.scatter(pca2[:,0], pca2[:,1], c=kmeans.labels_, cmap='viridis')

plt.show()
```

## Hierarchical clustering
<b><u>Hierarchical clustering on two columns</u></b>
```python
# Defining variables
y = convA[['difference']].values
x = convA[['total']].values
X = convA[['total', 'difference']].values
X

# Reference plot
print(X.shape)
plt.scatter(X[:,0], X[:,1])
plt.show()

# Clustering and checking Cophenetic Correlation Coefficient
z = linkage(x, 'average')
c, coph_dists = cophenet(z, pdist(x))
c

# Plot
idxs = [8,9,12]
plt.figure()
plt.scatter(X[:, 0], X[:, 1])
plt.scatter(X[idxs, 0], X[idxs, 1], c='r')

idxs = [10,11,13]
plt.scatter(X[idxs, 0], X[idxs, 1], c='y')

plt.show()

# Dendrogram
plt.figure(figsize=(25,10))
plt.title('Dendrogram')
dendrogram(z, leaf_rotation=90.,
           leaf_font_size=8.,)
plt.show()
```
<b><u>Hierarchical clustering on entire dataframe</u></b>
```python
print(pca2.shape)
plt.scatter(pca2[:,0], pca2[:,1])
plt.show()

# Clustering and checking Cophenetic Correlation Coefficient
z = linkage(pca2, 'average')
c, coph_dists = cophenet(z, pdist(pca2))
c

# Plot
idxs = [861,903,954]
plt.figure()
plt.scatter(pca2[:,0], pca2[:,1], alpha=0.1)
plt.scatter(pca2[idxs,0], pca2[idxs,1], c='r', alpha=0.5)

# idxs = [267,720,445]
# plt.scatter(pca2[idxs,0], pca2[idxs,1], c='y')

plt.show()

# Dendrogram
plt.figure(figsize=(25,10))
plt.title('Dendrogram')
dendrogram(z, leaf_rotation=90.,
           leaf_font_size=8.,)
plt.show()
```

## Gaussian mixture
```python
# Clustering and plotting
gmm = GaussianMixture(n_components=4).fit(x)
labels = gmm.predict(x)
plt.scatter(X[:,0], X[:,1], c=labels, cmap='viridis');

# Probability
probs = gmm.predict_proba(x)
print(probs[:5].round(3))

# Plotting again
size = 50 * probs.max(1) ** 2
plt.scatter(X[:,0], X[:,1], c=labels, cmap='viridis', s=size);
```
## KNN
<b><u>Using KNN on a small dataset</u></b>
```python
knn = clusteredM[['postcode1', '# converted',
    'total', 'difference', 'cat']]
knn.head()

# Splitting into attributes and features
X = knn.iloc[:, :-1].values
y = knn.iloc[:, 4].values
X

# Dividing the dataset
X_train, X_test, y_train, y_test =
    train_test_split(X, y,
    test_size=0.20, random_state=111)

# Scaling the features
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


# Training KNN
knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(X_train, y_train)

# Making predictions
y_pred = knn.predict(X_test)

# Evaluating KNN
knnConf1 = confusion_matrix(y_test, y_pred)
knnClass1 = classification_report(y_test, y_pred)

print(knnConf1)
print(knnClass1)
```
<b><u>Using KNN on entire dataset</u></b>
```python
knn2 = clusteredM[:]
knn2.head()

# Dropping unnecessary columns
knn2.drop(['% converted', 'label'],
    axis=1, inplace=True)
knn2.head()

# Splitting into attributes and features
X = knn2.iloc[:, :-1].values
y = knn2.iloc[:, 12].values
y

# Dividing the dataset
X_train, X_test, y_train, y_test =
    train_test_split(X, y,
    test_size=0.20, random_state=111)

# Scaling the features
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Training KNN
knn2 = KNeighborsClassifier(n_neighbors=4)
knn2.fit(X_train, y_train)

# Making predictions
y_pred = knn2.predict(X_test)

# Evaluating KNN
knnConf2 = confusion_matrix(y_test, y_pred)
knnClass2 = classification_report(y_test, y_pred)

print(knnConf2)
print(knnClass2)
```
