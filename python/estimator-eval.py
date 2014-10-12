#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error

def ints(s):
    res = []
    for ss in s:
        res.append(int(ss))
    return res

def sigmoid(p):
    return 1.0 / (1.0 + math.exp(-p))

def estimator_lr(feats):
    pred = 0.0
    for feat in feats:
        if feat in featWeight:
            pred += featWeight[feat]
    pred = sigmoid(pred)
    return pred

random.seed(10)

if len(sys.argv) < 3:
    print 'Usage: test.yzx.txt train.yzx.txt.lr.weight'
    exit(-1)

y = []
yp = []
featWeight = {}
#initialize the lr

fi = open(sys.argv[2], 'r')
for line in fi:
    s = line.strip().split()
    feat = int(s[0])
    weight = float(s[1])
    featWeight[feat] = weight
fi.close()

fi = open(sys.argv[1], 'r')
for line in fi:
    data = ints(line.strip().replace(":1", "").split())
    clk = data[0]
    mp = data[1]
    fsid = 2 # feature start id
    feats = data[fsid:]
    pred = estimator_lr(feats)
    y.append(clk)
    yp.append(pred)
fi.close()

# evaluation
auc = roc_auc_score(y, yp)
rmse = math.sqrt(mean_squared_error(y, yp))
print "algo\tauc\trmse"
print "lr" + '\t' + str(auc) + '\t' + str(rmse)

