import random
import numpy as np
import joblib
from typing import List


class RoutingMiddleWare():

    def __init__(self, system_model_name:str="system_model.joblib", artifacts:str="../../../../artifacts/") -> None:
        self.state_size = 1
        self.state = np.zeros(self.state_size, dtype=float)
        ######actions#######################
        self.b1 = 0
        self.p1 = random.randint(0,5)/5
        self.c1 = random.randint(1,5)

        ######services offered loads########
        self.l1 = 4

        ######services carried loads########
        self.cl1 = round(self.l1 * (1 - self.b1), 1)

        #######response times##############
        self.d1 = random.random()

        #######state######################
        self.state[0] = self.l1

        self.LD_counter = 0

        self.system_model_path = artifacts + system_model_name
        self.delay_models = joblib.load(self.system_model_path)

        self.load = [4,8,12]

    def get_state(self) -> np.ndarray:
        return self.state

    def read_state_from_system(self, action):
        action = np.array(action)
        action = np.squeeze(action)
        self.p1 = round(action[0] / 5, 1)
        self.c1 = action[1] + 1
        self.b1 = 0

        self.cl1 = round(self.l1 * (1 - self.b1), 1)

        # Feature list in the system model: ["max_l1", "l1", "cl1", "p1", "b1", "c1"]
        [self.d1] = self.delay_models.predict([[self.l1, self.l1 * 5, self.l1 * 5, self.p1, self.l1, self.c1]])

        if (self.LD_counter % 2 == 0):
            self.l1 = self.load[random.randint(0, len(self.load) - 1)]

        self.state[0] = self.l1

        self.LD_counter += 1
        return self.state, self.cl1, self.d1, round(self.c1, 1), round(self.p1, 1)

    def reset(self):
        self.LD_counter = 0
        return self.state

# test_routing = RoutingMiddleWare()
# for i in range(10):
#     print(test_routing.read_state_from_system([2,3]))