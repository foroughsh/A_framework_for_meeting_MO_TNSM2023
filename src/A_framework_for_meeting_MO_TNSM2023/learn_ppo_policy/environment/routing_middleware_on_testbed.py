import random
import time

import numpy as np
import joblib
from A_framework_for_meeting_MO_TNSM2023.data_collection.run_commands_on_cluster import RunCommandsOnCluster

import pandas as pd


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
        self.artifacts = artifacts

        # self.load = [4,8,12]
        self.load = np.array(pd.read_csv(artifacts + "random_load.csv")["l"])
        self.path_to_config_files = "../../../cluster_configuration_files/"

        self.time_step = 10
        self.settling_time = 10

    def get_state(self) -> np.ndarray:
        return self.state

    def read_loads(self):
        with open(self.artifacts + "load_compute.txt","r") as file:
            lines = file.readlines()
        file.close()

        return len(lines)

    def clean_file_contents(self) -> None:
        with open(self.artifacts + "load_compute.txt","w") as file:
            file.write("")
        file.close()
        with open(self.artifacts + "response_compute.txt","w") as file:
            file.write("")
        file.close()

    def read_stats(self):
        with open(self.artifacts + "response_compute.txt","r") as file:
            lines = file.readlines()
        file.close()
        responses_from_node_1 = []
        responses_from_node_2 = []
        drops = []
        for line in lines:
            req = eval(line)
            if (req["code"] == 200):
                if (req["Node"] == 1):
                    responses_from_node_1.append(req["response"])
                elif (req["Node"] == 2):
                    responses_from_node_2.append(req["response"])
            else:
                drops.append(req["response"])

        all_successful_response = responses_from_node_1 + responses_from_node_2
        cl1 = len(all_successful_response)
        if (len(responses_from_node_1) > 0):
            d11 = np.mean(responses_from_node_1)
            d11_std = np.std(responses_from_node_1)
        else:
            d11 = 0
            d11_std = 0

        if (len(responses_from_node_2) > 0):
            d12 = np.mean(responses_from_node_2)
            d12_std = np.std(responses_from_node_2)
        else:
            d12 = 0
            d12_std = 0

        if (len(all_successful_response) > 0):
            d1 = np.mean(all_successful_response)
            d1_99 = np.percentile(all_successful_response, 99)
            d1_90 = np.percentile(all_successful_response, 90)
            d1_std = np.std(all_successful_response)
        else:
            d1 = 0
            d1_99 = 0
            d1_90 = 0
            d1_std = 0

        drop1 = len(drops)
        statics = dict()
        statics["cl"] = cl1
        statics["d1"] = d11
        statics["d1_std"] = d11_std
        statics["d2"] = d12
        statics["d2_std"] = d12_std
        statics["d"] = d1
        statics["d_99"] = d1_99
        statics["d_90"] = d1_90
        statics["d_std"] = d1_std
        statics["drops"] = drop1
        return statics

    def apply_service_config(self) -> None:
        '''
        This function currently works only for one service since in the RunCommandsOnCluster paths are hard coded.
        Later we should add the name of the files for services so it can change the cofiguations for the services in the loop.
        :return:
        '''
        routing_weight = int(self.p1 * 100)
        scaling = self.c1
        command_runner = RunCommandsOnCluster(self.path_to_config_files)
        command_runner.set_routing_action(routing_weight)
        command_runner.set_scaling_action(scaling)
        command_runner.revise_routing_action()
        command_runner.run_routing_action()
        command_runner.revise_scaling_action()
        command_runner.run_scaling_action()

    def read_state_from_system(self, action):
        action = np.array(action)
        action = np.squeeze(action)
        print("Action is: ")
        self.p1 = round(action[0] / 5, 1) * 100
        self.c1 = action[1] + 1
        self.b1 = 0
        print("The routing weight and scaling actions are: ", self.p1, self.c1)

        time.sleep(self.settling_time)
        self.apply_service_config()
        self.clean_file_contents()
        time.sleep(self.time_step)
        self.l1 = self.read_loads()
        stats = self.read_stats()

        self.cl1 = stats["cl"]

        self.d1 = stats["d1"]

        self.state[0] = self.l1

        self.LD_counter += 1
        return self.state, self.cl1, self.d1, round(self.c1, 1), round(self.p1, 1)

    def reset(self):
        self.LD_counter = 0
        return self.state

# test_routing = RoutingMiddleWare()
# for i in range(10):
#     print(test_routing.read_state_from_system([2,3]))