import gym
from gym.envs.registration import register

register(
    id='routing-env-v2',
    entry_point='A_framework_for_meeting_MO_TNSM2023.learn_ppo_policy.environment.routing_env:RoutingEnv',
    kwargs={'path_to_system_model': None, 'path_to_artifacts': None}
)