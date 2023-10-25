import random
from typing import Tuple
import gym
import gymnasium
import numpy as np
from TNSM2023.learn_ppo_policy.environment.routing_middle_ware import RoutingMiddleWare
from typing import List

class RoutingEnv(gym.Env):

    def __init__(self, path_to_system_model:str, path_to_artifacts:str) -> None:
        self.observation_space = gym.spaces.Box(low=np.array([0]), dtype=np.float32,
                                                high=np.array([15]),
                                                shape=(1,))
        self.action_space = gym.spaces.MultiDiscrete([6,5])
        self.middleware = RoutingMiddleWare(path_to_system_model, path_to_artifacts)

        self.O1 = 1.0

        self.l1 = 4
        self.cl1 = self.l1

        self.d1 = random.random()

        self.c1 = 1
        self.p1 = 1

        self.s = [self.l1]
        self.t = 1
        self.reset()

    def step(self, a: gym.spaces.MultiDiscrete) -> Tuple[np.ndarray, int, bool, dict]:
        info = {}
        done = False
        next_state, cl1, d1, c1, p1 = self.middleware.read_state_from_system(a)
        l1 = next_state[0]
        cl1 = l1

        self.d1 = d1
        self.c1 = c1
        self.p1 = p1

        reward = self.reward_function()

        info["l1"] = l1
        info["cl1"] = cl1
        info["d1"] = d1
        info["cpu1"] = c1
        info["p1"] = p1

        self.l1 = l1
        self.cl1 = cl1

        self.d1 = d1

        self.p1 = p1
        self.s = next_state

        info["r"] = reward
        # if self.t > 10:
        #     done = True
        self.t += 1

        return np.array([self.l1]), reward, done, info

    def reset(self) -> np.ndarray:
        self.t = 1

        self.middleware.reset()

        state, cl1, d1, c1, p1 = self.middleware.read_state_from_system([0,0])

        self.l1 = state[0]
        self.cl1 = cl1
        self.p1 = p1
        self.c1 = c1

        self.d1 = d1

        self.s = state
        return np.array([self.l1])

    def reward_function(self):
        d1 = round(self.d1, 3) + 0.6
        reward = 0
        if (d1 <= self.O1):
            reward = 6 - self.c1
        else:
            if (d1 > self.O1):
                reward = self.O1 - d1
        return round(reward, 3)

# env = RoutingEnv("system_model.joblib", "../../../../artifacts/")
# for i in range(0,10):
#     print("Step ----> ", i)
#     action = [random.randint(0,5), random.randint(0,4)]
#     print("In the loop:",action)
#     s, reward, done, info = env.step(action)
#     print(s, reward, done, info)
