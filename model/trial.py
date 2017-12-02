from sklearn import svm
from sklearn.linear_model import Lasso
from util import *
from sklearn.externals import joblib

features, labels = load_feature_vectors(fname='../norm_data.csv', wanted_labels=['BRONZE', 'SILVER', 'GOLD', 'PLATINUM'])

labels2 = []
for i in xrange(len(features)):
    vec = []
    for w in ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']:
        vec.append(labels[w][i])
    labels2.append(vec)

features = np.array(features)
labels2 = np.array(map(lambda x: x[1], labels2)).reshape(-1, 1)

# print features.shape, labels2.shape

# model = svm.SVR()
# model.fit(features, labels)
# joblib.dump(model, 'testsvm.pkl') 
# print model.predict(arr)
# print features[0].shape

# # load
# model = joblib.load('testsvm.pkl') 
# print model.predict(features[0].reshape(1, -1)),  labels[0]

# clf = Lasso(alpha=0.0005)
# clf.fit(features, labels2)
# print clf.coef_

lsvc = svm.LinearSVR()
lsvc.fit(features, labels2)
joblib.dump(lsvc, 'lsvc1.pkl') 
print lsvc.coef_