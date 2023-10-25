import random
import pandas as pd
import torch
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import gym
from stable_baselines3.common.callbacks import BaseCallback
import scipy.stats as st
import sys
import argparse
from TNSM2023.learn_ppo_policy.environment.routing_env import RoutingEnv


class CustomCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """
    def __init__(self, seed: int, verbose=0, eval_every: int = 200):
        super(CustomCallback, self).__init__(verbose)
        self.iter = 0
        self.eval_every = eval_every
        self.seed = seed

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        pass

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """
        return True

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        print(f"Training iteration: {self.iter}")
        if self.iter % self.eval_every == 0:
            s = self.training_env.reset()
            max_horizon = 10
            done = False
            t = 0
            rewards = []
            optimal_rewards = []
            while not done and t <= max_horizon:
                a, _ = model.predict(s, deterministic=True)
                s, r, done, info = env.step(a)
                opt_r = optimal[s[0]]
                rewards.append(r)
                optimal_rewards.append(opt_r)
                t+= 1
            avg_R = np.mean(rewards)
            std_R = np.std(rewards)
            avg_optimal_R = np.mean(optimal_rewards)
            (lower, upper) = st.t.interval(alpha=0.95, df=len(rewards) - 1, loc=np.mean(rewards), scale=st.sem(rewards))
            with open(f"avg_reward_{self.seed}.csv", 'a') as file:
                line = str(avg_R) + "," + str(std_R) + "," + str(lower) + "," + str(upper) + "," + str(avg_optimal_R) + "\n"
                file.write(line)
            file.close()
            print(f"[EVAL] Training iteration: {self.iter}, Average R:{avg_R}")
            self.training_env.reset()
            model.save("self_routing_" + str(self.iter))
        self.iter += 1

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass

if __name__ == '__main__':
    args = sys.argv

    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--system_model", type=str, default="system_model.joblib")
    parser.add_argument("--optimal_policy", type=str, default="optimal_policy.csv")

    args = parser.parse_args()

    artifacts = args.artifacts
    system_model = args.system_model
    optimal_policy = args.optimal_policy

    optimal_rewards = pd.read_csv(artifacts + optimal_policy)
    optimal = dict()
    for i in range(optimal_rewards.shape[0]):
        optimal[optimal_rewards["l"].iloc[i]] = optimal_rewards["r"].iloc[i]

    env = gym.make("routing-env-v2", path_to_system_model=system_model, path_to_artifacts=artifacts)
    env = Monitor(env)

    # Hparams
    num_neurons_per_hidden_layer = 64
    num_layers = 3
    policy_kwargs = dict(net_arch=[num_neurons_per_hidden_layer] * num_layers)
    steps_between_updates = 512  # 512#128
    learning_rate = 0.0005
    batch_size = 64
    device = "cpu"
    gamma = 0
    num_training_timesteps = int(50000)
    verbose = 0
    # ent_coef = 0.05
    # clip_range = 0.2

    # Set seed for reproducibility
    seed = 999
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Creating file for the outputs.
    with open(f"avg_reward_{seed}.csv", "w") as file:
        file.write("avg_r,std_r,lower_r,upper_r,avg_optimal_r\n")
    file.close()

    cb = CustomCallback(seed=seed, eval_every=2)

    # Train
    model = PPO("MlpPolicy", env, verbose=verbose,
                policy_kwargs=policy_kwargs, n_steps=steps_between_updates,
                batch_size=batch_size, learning_rate=learning_rate, seed=seed,
                device="cpu", gamma=gamma)
    model.learn(total_timesteps=num_training_timesteps, callback=cb)
