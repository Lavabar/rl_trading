"""
    the sequence of stocks is: ('AAPL', 'IBM', 'MSFT')
"""

from TradeAPI import TestApp, IBcontract, Order
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import itertools
import requests
import time

class TradingEnv(gym.Env):
    def __init__(self):
        # connecting to broker
        self.app = TestApp("127.0.0.1", 7497, 1)
        self.accountName = "DU229537"
        self.idx_CashBalance = 19
        self.idx_NetLiquidation = 96
        accounting_values = self.app.get_accounting_values(self.accountName)

        # data
        self.n_stock = 3

        # instance attributes
        self.real_cash = float(accounting_values[self.idx_CashBalance][1])
        self.init_invest = self.real_cash - 300000
        self.stock_owned = None
        self.stock_price = None
        self.cash_in_hand = None

        # action space
        self.action_space = spaces.Discrete(3**self.n_stock)

        self.observation_space_shape = 7
        # seed and start
        self._seed()
        #self.reset()
        self.symbols = ['AAPL', 'IBM', 'MSFT']
        with open("/home/user/projects/your_dream/AV_token.txt", "r") as f:
            self.AV_api_key = f.readline()

    def __del__(self):
        self.app.disconnect()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def update(self):
        accounting_updates = self.app.get_accounting_updates(self.accountName)
        self.stock_owned = [accounting_updates[j][1] for j in range(self.n_stock)]
        stock_prices = []
        stock_prices.append(self._get_cur_price(self.symbols[0]))
        stock_prices.append(self._get_cur_price(self.symbols[1]))
        stock_prices.append(self._get_cur_price(self.symbols[2]))
        self.stock_price = stock_prices
        accounting_values = self.app.get_accounting_values(self.accountName)
        self.cash_in_hand = float(accounting_values[self.idx_CashBalance][1]) - 300000.0

        return self._get_obs()


    def step(self, action):
        assert self.action_space.contains(action)
        prev_val = self._get_val()
        self.update()
        #self.stock_price = self.stock_price_history[:, self.cur_step] # update price
        self._trade(action)
        cur_val = self._get_val()
        reward = cur_val - prev_val
        accounting_values = self.app.get_accounting_values(self.accountName)
        if float(accounting_values[self.idx_CashBalance][1]) - 300000.0 == 0:
            done = True
        else:
            done = False
        info = {'cur_val': cur_val}
        return reward, done, info


    def _get_obs(self):
        obs = []
        obs.extend(self.stock_owned)
        obs.extend(self.stock_price)
        obs.append(self.cash_in_hand)
        return obs


    def _get_val(self):
        return np.sum(np.asarray(self.stock_owned) * np.asarray(self.stock_price)) + self.cash_in_hand


    def _trade(self, action):
        # all combo to sell(0), hold(1), or buy(2) stocks
        action_combo = list(map(list, itertools.product([0, 1, 2], repeat=self.n_stock)))
        action_vec = action_combo[action]
        print(action_vec)
        # one pass to get sell/buy index
        sell_index = []
        buy_index = []
        for i, a in enumerate(action_vec):
            if a == 0:
                sell_index.append(i)
            elif a == 2:
                buy_index.append(i)

        # two passes: sell first, then buy; might be naive in real-world settings
        if sell_index:
            for i in sell_index:
                cnt = self._init_contract(self.symbols[i])
                ordId = self._make_order(cnt, "SELL", self.stock_owned[i])
                self.update()
        if buy_index:
            for i in buy_index:
                cnt = self._init_contract(self.symbols[i])
                ordId = self._make_order(cnt, "BUY", self.cash_in_hand // (self.stock_price[i]))
                self.update()

    def _get_cur_price(self, symbol):
        time.sleep(12)
        req = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol + "&interval=1min&apikey=" + self.AV_api_key
        res = requests.get(req)
        data = res.json()

        #print(data)
        idx1 = 'Time Series (1min)'
        idx2 = [i for i in data[idx1]]

        return float(data[idx1][idx2[0]]['4. close'])

    def _init_contract(self, symbol):
        ibcontract = IBcontract()
        ibcontract.secType = "STK"
        #ibcontract.lastTradeDateOrContractMonth="201812"
        ibcontract.symbol=symbol
        ibcontract.exchange="SMART"
        ## resolve the contract
        resolved_ibcontract = self.app.resolve_ib_contract(ibcontract)

        return resolved_ibcontract

    def _make_order(self, contract, action, quantity):
        order = Order()
        order.orderType = "MKT"
        order.action = action
        order.totalQuantity = quantity
        order.transmit = True

        orderid = self.app.place_new_IB_order(contract, order, orderid=None)

        return orderid