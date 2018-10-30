import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def get_data(mode, col='close'):
  """ Returns a 3 x n_step array """
  if mode == "train":
    msft = pd.read_csv('data/msft.csv', usecols=[col])
    aapl = pd.read_csv('data/aapl.csv', usecols=[col])
    ibm = pd.read_csv('data/ibm.csv', usecols=[col])
  elif mode == "test":
    msft = pd.read_csv('test_data/msft.csv', usecols=[col])
    aapl = pd.read_csv('test_data/aapl.csv', usecols=[col])
    ibm = pd.read_csv('test_data/ibm.csv', usecols=[col])

  # recent price are at top; reverse it
  return np.array([msft[col].values[::-1],
                   ibm[col].values[::-1],
                   aapl[col].values[::-1]])


def get_scaler(env):
  """ Takes a env and returns a scaler for its observation space """
  low = [0] * (env.n_stock * 2)
  low.extend([-1, -1, -1])
  low.append(0)

  high = []
  max_price = 2000
  min_price = 100
  #max_cash = env.real_cash ### for testing, not training
  max_cash = env.init_invest * 3
  max_stock_owned = max_cash // min_price
  for i in range(env.n_stock):
    high.append(max_stock_owned)
  for i in range(env.n_stock):
    high.append(max_price)
  high.extend([1, 1, 1])
  high.append(max_cash)

  scaler = StandardScaler()
  scaler.fit([low, high])
  return scaler


def maybe_make_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)