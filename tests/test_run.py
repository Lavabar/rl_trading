import sys
sys.path.append("../")

import pickle
import time
import numpy as np
import argparse
import re

from real_envs import TradingEnv
from agent import DQNAgent
from utils import get_data, get_scaler, maybe_make_dir

if __name__ == '__main__':
    weights = "/home/user/projects/your_dream/weights/201810202030-dqn.h5"
    #maybe_make_dir('weights')

    timestamp = time.strftime('%Y%m%d%H%M')

    # remake the env with test data
    env = TradingEnv()
    state_size = env.observation_space_shape
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size, "test")
    
    # load trained weights
    agent.load(weights)
    # when test, the timestamp is same as time when weights was trained
    timestamp = re.findall(r'\d{12}', weights)[0]

    state = env.update()
    scaler = get_scaler(env)
    state = scaler.transform([state])
    print(state)
    
    reward, done, info = env.step(0)
    
'''    action = agent.act(state)
    next_state, reward, done, info = env.step(action)
    print(next_state)
    next_state = scaler.transform([next_state])
    print(next_state)'''