# A Framework for dynamically meeting performance objectives on a service mesh

![version](https://img.shields.io/badge/version-1.0.0-blue) ![license](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green) [![PyPI version](https://badge.fury.io/py/online-policy-adaptation-using-rollout.svg)](https://badge.fury.io/py/online-policy-adaptation-using-rollout) ![PyPI - Downloads](https://img.shields.io/pypi/dm/online-policy-adaptation-using-rollout)

We introduce a comprehensive framework designed to achieve end-to-end management objectives for multiple services concurrently operating within a service mesh. Leveraging reinforcement learning (RL) techniques, our framework trains an agent to periodically execute control actions for resource reallocation. Our development and evaluation take place within a laboratory testbed where information and computing services run on a service mesh supported by Istio and Kubernetes platforms.

Our investigation encompasses various management objectives, including enforcing end-to-end delay bounds on service requests, optimizing throughput, managing cost-related objectives, and implementing service differentiation. Notably, we compute control policies on a simulator instead of the testbed, significantly expediting the training process for the scenarios under study.

Distinguishing itself by advocating a top-down approach, our framework prioritizes the definition of management objectives before mapping them onto available control actions. This approach enables the concurrent execution of multiple control actions and facilitates training the agent for diverse management objectives in parallel by initially learning the system model and operating region from testbed traces.

<p align="center">
<img src="https://github.com/foroughsh/TNSM2023/blob/master/framework_all_components%20(5).png" width="500"/>
</p>

## Requirements

- `gym` and `gymnasium`: for creating the RL environments
- `joblib`: for loading/exporting random forest regressor models
- `sb3-contrib`: for reinforcement learning agents (Maskable PPO)
- `scikit-learn`: for random forest regression
- `scipy`: for random forest regression
- `stable-baselines3`: for reinforcement learning agents (PPO)
- `torch` and `torchvision`: for neural network training
- `matplotlib`: for plotting
- `pandas`: for data wrangling
- `requests`: for making HTTP requests

## Development Requirements

- Python 3.7+
- `flake8` (for linting)
- `tox` (for automated testing)

## Copyright and license

<p>
<a href="./LICENSE.md">Creative Commons (C) 2021-2024, Forough Shahabsamani</a>
</p>

## Authors & Maintainers

- Forough Shahabsamani <foro@kth.se>
