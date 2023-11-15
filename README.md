# A Framework for dynamically meeting performance objectives on a service mesh

![version](https://img.shields.io/badge/version-1.0.0-blue) ![license](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green) [![PyPI version](https://badge.fury.io/py/online-policy-adaptation-using-rollout.svg)](https://badge.fury.io/py/online-policy-adaptation-using-rollout) ![PyPI - Downloads](https://img.shields.io/pypi/dm/online-policy-adaptation-using-rollout)

Dynamic resource allocation in networked systems is necessary to achieve end-to-end management objectives. Previous research has demonstrated that reinforcement learning is a promising approach to this problem, allowing to obtain near-optimal resource allocation policies for non-trivial system configurations. Despite these advances, a significant drawback of current approaches is that they require expensive and slow retraining whenever the target system changes. We address this drawback and introduce an efficient approach to adapt a given base policy to dynamic system changes. In our approach, we adapt the base policy through rollout and online play, which transforms the base policy into a rollout policy. 

The following figure shows our approach for policy adaptation in networked systems. During each control cycle, the system model $f$ is estimated from system metrics using supervised learning; a given base policy $\hat{\pi}$ is adapted for the current state and the current system model through one step of policy iteration, which we call rollout and the output of this step is an improved rollout policy $\tilde{\pi}$ which is used to select the next control action.

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


## Run Experiments

### Scenario 1

```bash
cd examples; python run_scenario_1.py
```

### Scenario 2
```bash
cd examples; python run_scenario_2.py
```

### Scenario 3
```bash
cd examples; python run_scenario_3.py
```

## Copyright and license

<p>
<a href="./LICENSE.md">Creative Commons (C) 2023-2024, Forough Shahabsamani</a>
</p>

## Authors & Maintainers

- Forough Shahabsamani <foro@kth.se>
