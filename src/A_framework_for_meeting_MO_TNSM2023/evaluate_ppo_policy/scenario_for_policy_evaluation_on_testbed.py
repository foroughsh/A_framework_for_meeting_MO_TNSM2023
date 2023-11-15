import time
from typing import List
from A_framework_for_meeting_MO_TNSM2023.data_collection.data_collection import DataCollection
import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import gym
import pandas as pd
import numpy as np
from A_framework_for_meeting_MO_TNSM2023.learn_ppo_policy.environment.routing_env import RoutingEnv

def read_load_from_file(file_name:str) -> List[int]:
    load = []
    with open(file_name, "r") as file:
        lines = file.readlines()

    for line in lines:
        load.append(int(line))

    return load

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--path_to_artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--data_file_name", type=str, default="data_evaluation.csv")
    parser.add_argument("--path_to_LG", type=str, default="../data_collection/")
    parser.add_argument("--load_file_name", type=str, default="random_load.csv")
    parser.add_argument("--IP_port", type=str, default="172.31.212.81:30048")
    parser.add_argument("--path_to_config_file", type=str, default="../../../cluster_configuration_files/")
    parser.add_argument("--ppo_policy_name", type=str, default="self_routing_48.zip")
    parser.add_argument("--system_model", type=str, default="system_model.joblib")

    args = parser.parse_args()

    path_to_artifacts = args.path_to_artifacts
    path_to_LG = args.path_to_LG
    path_to_load = args.load_file_name
    IP_port = args.IP_port
    output_file = args.data_file_name
    path_to_config_file = args.path_to_config_file
    ppo_policy_name = args.ppo_policy_name
    system_model = args.system_model

    service = dict()
    service["name"] = "compute"
    service["l"] = 1
    service["p"] = 80
    service["b"] = service["l"]
    service["c"] = 1
    services = [service]

    data_collection = DataCollection(IP_port=IP_port, data_file_name="no.csv", path_to_artifacts=path_to_artifacts,
                                     path_to_LG=path_to_LG, path_to_config_files=path_to_config_file, services=services,
                                     n=1)

    data_collection.kill_load_generator()
    load = np.array((pd.read_csv(path_to_artifacts + path_to_load))["l"])

    ppo_model_name = path_to_artifacts + ppo_policy_name

    env = gym.make("routing-env-v2", path_to_system_model=system_model, path_to_artifacts=path_to_artifacts)
    env = Monitor(env)

    model = PPO.load(ppo_model_name)

    obs = env.reset()
    evaluation_step = 0

    with open(path_to_artifacts + output_file, "w") as file:
        file.write("load,rewards,d1,c1,p1,action\n")
    file.close()

    for l in load:
        service["l"] = l
        data_collection.set_services(services=[service])
        data_collection.run_load_generator(service["name"], l)
        print("The load value is: ", l)
        for j in range(10):
            obs=np.array([l])
            action, _states = model.predict(obs, deterministic=True)  # ,
            obs, rewards, dones, info = env.step(action)
            evaluation_step += 1
            with open(path_to_artifacts + output_file, "a") as file:
                line = str(l) + "," + str(rewards) + "," + str(info["d1"]) + "," + str(info["cpu1"]) + "," + str(info["p1"]) + "," + str(action) + "\n"
                file.write(line)
            file.close()
            print(line)
        data_collection.kill_load_generator()
