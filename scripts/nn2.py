import numpy as np
import csv
import pandas as pd
df = pd.read_csv('bikeset.csv')
df["N_Traffic"] = df["N_Traffic"].map({'North_Abnormal':1 ,'North_normal':0})
df["NE_Traffic"] = df["NE_Traffic"].map({'NE_Abnormal':1 ,'NE_Normal':0})
df["E_Traffic"] = df["E_Traffic"].map({'East_Abnormal':1 ,'East_normal':0})
df["SE_Traffic"] = df["SE_Traffic"].map({'SE_Abnormal':1 ,'SE_normal':0})
df["S_Traffic"] = df["S_Traffic"].map({'South_Abnormal':1 ,'South_normal':0})
df["SW_Traffic"] = df["SW_Traffic"].map({'SW_Abnormal':1 ,'SW_normal':0})
df["W_Traffic"] = df["W_Traffic"].map({'West_Abnormal':1 ,'West_normal':0})
df["NW_Traffic"] = df["NW_Traffic"].map({'NW_Abnormal':1 ,'NW_normal':0})
df["Importance?"] = df["Importance?"].map({'Important':1 ,'Normal':0})
imp_data = df[["N_Traffic","NE_Traffic","E_Traffic","SE_Traffic","S_Traffic","SW_Traffic","W_Traffic","NW_Traffic","Importance?"]].to_numpy()
feature_set = imp_data[:, [0,1,2,3,4,5,6,7]]
labels = imp_data[:, [8]]
np.random.seed(42)  
weights = np.random.rand(8,1)  
bias = np.random.rand(1)  
lr = 0.2
def sigmoid(x):  
    return 1/(1+np.exp(-x))
def sigmoid_der(x):  
    return sigmoid(x)*(1-sigmoid(x))
epoch = 1
x = 1
#print(weights,bias)
for epoch in range(2000):
#while (abs(x) > .001):  
    inputs = feature_set

    # feedforward step1
    XW = np.dot(feature_set, weights) + bias

    #feedforward step2
    z = sigmoid(XW)


    # backpropagation step 1
    error = z - labels
    x = error.sum()
    #print(epoch,x)

    # backpropagation step 2
    dcost_dpred = error
    dpred_dz = sigmoid_der(z)

    z_delta = dcost_dpred * dpred_dz

    inputs = feature_set.T
    weights -= lr * np.dot(inputs, z_delta)

    for num in z_delta:
        bias -= lr * num
    #epoch = epoch + 1
#print(weights,bias,x)
print('%ge of Accuracy of the system is:',((1.0-abs(x/1000.0))*100.0))
to_predict = np.array([1,1,1,1,1,1,1,1])  
result = sigmoid(np.dot(to_predict, weights) + bias)  
print('Importance of the station with the the data set:1,1,1,1,1,1,1,1,1 is:',result)
to_predict = np.array([1,0,0,1,0,0,0,1])  
result = sigmoid(np.dot(to_predict, weights) + bias)  
print('Importance of the station with the the data set:1,0,0,1,0,0,0,1 is:',result)
to_predict = np.array([1,0,1,0,1,1,1,1])  
result = sigmoid(np.dot(to_predict, weights) + bias)  
print('Importance of the station with the the data set:1,0,1,0,1,1,1,1 is:',result)
