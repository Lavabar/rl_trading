import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def get_data(col='close'):
  """ Returns a 3 x n_step array """
  msft = pd.read_csv('data/msft.csv', usecols=[col])
  aapl = pd.read_csv('data/aapl.csv', usecols=[col])
  ibm = pd.read_csv('data/ibm.csv', usecols=[col])
  # recent price are at top; reverse it
  return np.array([msft[col].values[::-1],
                   ibm[col].values[::-1],
                   aapl[col].values[::-1]])


def get_scaler(env):
  """ Takes a env and returns a scaler for its observation space """
  low = [0] * (env.n_stock * 2 + 1)

  high = []
  max_price = 2000
  min_price = 100
  max_cash = env.real_cash
  max_stock_owned = max_cash // min_price
  for i in range(env.n_stock):
    high.append(max_stock_owned)
  for i in range(env.n_stock):
    high.append(max_price)
  high.append(max_cash)

  scaler = StandardScaler()
  scaler.fit([low, high])
  return scaler


def maybe_make_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)