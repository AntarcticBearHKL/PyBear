from sklearn.svm import SVC


class Spliter:
    def __init__(self):
        pass

class BSVC:
    def __init__(self):
        pass

    def st():
        model = SVC(kernel='linear', C=1E10)
        X=[
            [5,2],
            [7,2],
            [12,2],
            [14,2],
            [24,2],
            [25,2],
        ]
        y=[1,1,2,2,3,3]
        model.fit(X, y)
        print(model.predict([[21,2]]))
        joblib.dump(model, 'model.pkl')


class Judger:
    def __init__(self):
        pass