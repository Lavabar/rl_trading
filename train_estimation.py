import numpy as np
from model import lstm
from utils import get_data

def make_dataset(data, history_length, n_stock):
    n = data.shape[1] - history_length
    X_train = np.zeros((n, history_length, n_stock))
    Y_train = np.zeros((n, n_stock))

    for i in range(n):
        X_train[i] = data.T[(0 + i):(history_length + i), :]
        Y_train[i] = data.T[history_length + i, :]
    
    X_train_n = np.split(X_train, n_stock, axis=2)
    Y_train_n = np.split(Y_train, n_stock, axis=1)
    
    max_price = data.max(axis=1)

    X_train1 = X_train_n[0] / max_price[0]
    X_train2 = X_train_n[1] / max_price[1]
    X_train3 = X_train_n[2] / max_price[2]

    Y_train1 = Y_train_n[0]
    Y_train2 = Y_train_n[1]
    Y_train3 = Y_train_n[2]


    Y_train1 = np.subtract(Y_train1, X_train1[:, X_train1.shape[1] - 1]) / Y_train1
    Y_train2 = np.subtract(Y_train2, X_train2[:, X_train2.shape[1] - 1]) / Y_train2
    Y_train3 = np.subtract(Y_train3, X_train3[:, X_train3.shape[1] - 1]) / Y_train3

    X_train_norm = [X_train1, X_train2, X_train3]
    Y_train_norm = [Y_train1, Y_train2, Y_train3]


    return X_train_norm, Y_train_norm

data = get_data()
#print(data.shape)
X_train, Y_train = make_dataset(data, 10, 3)

model = lstm(X_train[0].shape)
model1 = lstm(X_train[1].shape)
model2 = lstm(X_train[2].shape)

model.summary()
model1.summary()
model2.summary()

model.fit(X_train[0], Y_train[0], epochs=10)
model.save_weights(filepath="aapl.weights")

model1.fit(X_train[1], Y_train[1], epochs=10)
model1.save_weights(filepath="ibm.weights")

model2.fit(X_train[2], Y_train[2], epochs=10)
model2.save_weights(filepath="msft.weights")