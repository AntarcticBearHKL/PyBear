from sklearn.svm import SVC

model = SVC(kernel='linear', C=1E10)
model.fit(X, y)