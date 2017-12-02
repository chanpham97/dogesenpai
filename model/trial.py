from sklearn import svm
from sklearn.linear_model import Lasso, LogisticRegression
from util import *
from sklearn.externals import joblib

# features, labels = load_feature_vectors(fname='../lasso_datahot.csv', wanted_labels=['BRONZE', 'SILVER', 'GOLD', 'PLATINUM'])

# labels2 = []
# for i in xrange(len(features)):
#     vec = []
#     for w in ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']:
#         vec.append(labels[w][i])
#     labels2.append(vec)

# features = np.array(features)
# labels2 = np.array(map(lambda x: x[1], labels2)).reshape(-1, 1)

# print features.shape, labels2.shape

# model = svm.SVR()
# model.fit(features, labels)
# joblib.dump(model, 'testsvm.pkl') 
# print model.predict(arr)
# print features[0].shape

# load
# model = joblib.load('testsvm.pkl') 
# print model.predict(features[0].reshape(1, -1)),  labels[0]

# clf = Lasso(alpha=0.005)
# clf.fit(features, labels2)
# print clf.coef_

X, y, X2, y2 = get_feature_sets_classification(nn=False)

# lsvc = svm.LinearSVR()
# lsvc.fit(features, labels2)
# joblib.dump(lsvc, 'lsvc1.pkl') 
# print lsvc.coef_

m = LogisticRegression(penalty='l1', C=100)
m.fit(X, y)
print m.coef_
print m.score(X, y)
print m.score(X2, y2)