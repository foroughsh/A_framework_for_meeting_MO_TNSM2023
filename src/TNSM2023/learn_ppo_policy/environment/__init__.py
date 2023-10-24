import gym
from gym.envs.registration import register

register(
    id='routing-env-v2',
    entry_point='TNSM2023.learning_ppo_policy.environment.env.routing_env:RoutingEnv',
    kwargs={'path_to_system_model': None, 'path_to_artifacts': None}
)