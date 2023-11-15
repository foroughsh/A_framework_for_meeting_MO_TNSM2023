import sys
import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import gym
import pandas as pd
import numpy as np
from A_framework_for_meeting_MO_TNSM2023.learn_ppo_policy.environment.routing_env import RoutingEnv

if __name__ == "__main__":
    args = sys.argv

    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--optimal_file_name", type=str, default="optimal_policy.csv")
    parser.add_argument("--artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--system_model", type=str, default="system_model.joblib")
    parser.add_argument("--output_file_name", type=str, default="output_file_name.csv")
    parser.add_argument("--ppo_policy_name", type=str, default="self_routing_48.zip") #14 is also good
    parser.add_argument("--load_name", type=str, default="random_load.csv")


    args = parser.parse_args()

    optimal_file_name = args.optimal_file_name
    artifacts = args.artifacts
    system_model = args.system_model
    output_file_name = args.output_file_name
    ppo_policy_name = args.ppo_policy_name
    load_name = args.load_name

    ppo_model_name = artifacts + ppo_policy_name

    load = pd.read_csv(artifacts + load_name)

    env = gym.make("routing-env-v2", path_to_system_model=system_model, path_to_artifacts=artifacts)
    env = Monitor(env)

    model = PPO.load(ppo_model_name)

    obs = env.reset()
    evaluation_step = 0

    with open(artifacts + output_file_name, "w") as file:
        file.write("load,rewards,d1,c1,p1,action\n")
        for l in load["l"]:
            print("The load value is: ", l)
            obs=np.array([l])
            action, _states = model.predict(obs, deterministic=True)  # ,
            obs, rewards, dones, info = env.step(action)
            print(obs, rewards, dones, info)
            evaluation_step += 1
            line = str(l) + "," + str(rewards) + "," + str(info["d1"]) + "," + str(info["cpu1"]) + "," + str(info["p1"]) + "," + str(action) + "\n"
            file.write(line)
    file.close()
