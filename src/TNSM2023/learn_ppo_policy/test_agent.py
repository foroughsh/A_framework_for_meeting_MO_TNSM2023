import gym
import numpy as np
from TNSM2023.learn_ppo_policy.environment.routing_env import RoutingEnv

if __name__ == '__main__':
    env = gym.make("routing-env-v2")
    s = env.reset()
    s = env.reset_to_specific_state(1,1,2000,2000)
    done = False
    t = 0
    print(s)
    while not done:
        raw_input = input("> ")
        raw_input = raw_input.strip()
        parts = raw_input.split(",")
        a = list(map(lambda x: float(x), parts))
        print(f"action: {a}")
        s, r, done, info = env.step(a)
        print(f"a:{a}, s:{s}, r:{r}, done{done}, info:{info}")
        t+= 1
