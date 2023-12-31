# Data collection on the testbed to learn the system model

One of the important steps in our framework is the learning model. The system model is a function that maps the current state of the system and the control action to the next state.

```math
s_{t+1} \triangleq f(s_t, a_t, w_t, t) \ \ t=1,2,...
```

where $f$ is a Markovian system model, $w_t \in \mathcal{W}$ is a random disturbance, and $a_t$ is the control action at time $t$, which is defined as

```math
a_t \triangleq ((a^{(p)}_{(j,k),i,t}, a^{(b)}_{i,t}, a^{(c)}_{j,t}))_{i \in \mathscr{S}, (j,k) \in \mathcal{E}, k,j \in \mathcal{V}}
```

where 
```math
a^{(p)}_{(j,k),i,t} \in \{0, \Delta_p, 2\Delta_p\, ...\}
```
indicates the change in routing weight for edge $(j,k)$ and service $S_i$, 
```math
a^{(b)}_{i,t} \in \{0, \Delta_b, 2\Delta_b\, ...\}
```
indicates the change in blocking rate for service $S_i$, and 
```math
a^{(c)}_{j,t} \in \{0, \Delta_c, 2\Delta_c\, ...\}
```
indicates the change in allocated CPU cores for node $j$.

We can also, take sequential actions (multi-step actions) defined as:

```math
a_t \triangleq ((a^{(p)}_{(j,k),i,t}, a^{(b)}_{i,t}, a^{(c)}_{j,t}))_{i \in \mathscr{S}, (j,k) \in \mathcal{E}, k,j \in \mathcal{V}}
```

where 
```math
a^{(p)}_{(j,k),i,t} \in \{-\Delta_p, 0, \Delta_p\} 
```
indicates the change in routing weight for edge $(j,k)$ and service $S_i$, 
```math
a^{(b)}_{i,t} \in \{-\Delta_b, 0, \Delta_b\} 
```
indicates the change in blocking rate for service $S_i$, and 
```math
a^{(c)}_{j,t} \in \{-\Delta_c,0,\Delta_c\} 
```
indicates the change in allocated CPU cores for node $j$.

Currently, the sequestional action set is not merged in the current repository. It can be accessed through the code presented in the following repository:
https://github.com/foroughsh/online_policy_adaptation_using_rollout

Given (\ref{eq:action_def}), the system model (\ref{eq:dynamics_def}) can be stated more explicitly as

```math
w_{t+1} \sim P(\cdot \mid s_t, a_t) \newline
```
```math
l_{i,t+1} = \lambda_i(t+1,w_{t+1}) i \in \mathscr{S}  \newline
```
```math
d_{i,t+1} = \alpha_i(s_{t},a_t, w_{t+1}) i \in \mathscr{S}  \newline
```
```math
p_{(j,k),i,t+1} = p_{(j,k),i,t} + a^{(p)}_{(j,k),i,t}  i \in \mathscr{S}, (j,k) \in \mathcal{E} \newline
```
```math
b_{i,t+1} = b_{i,t} + a^{(p)}_{i,t}   i \in \mathscr{S} \newline
```
```math
c_{j,t+1} = c_{j,t} + a^{(c)}_{j,t}  k \in \mathcal{V} 
```

where $t=1,2,...$, $w_{t+1} \sim P(\cdot \mid s_t, a_t)$ denotes that $w_{t+1}$ is sampled from $P$, and $\alpha_i$ is a function that models the response time of service $S_i$.

Considering the state values and actions (configuration parameters), we load the application with the specified values of load depending on the scenario change in the configuration of the system. After applying the change in the control action, we wait until the settling time of the action has elapsed. This time for the routing action is a fraction of a second and for the scaling, we consider 30 seconds. We learn the system state over the monitoring time that we consider 5 seconds in all scenarios. In the following figure, we show the relation between the action settling time and monitoring time.  

<p align="center">
<img src="https://github.com/foroughsh/online_policy_adaptation_using_rollout/blob/main/documentation/images/time_step.png" width="500"/>
</p>

The main reason is that during the settling time, the response time is not stable and stationary. As it is shown in the following image.

<p align="center">
<img src="https://github.com/foroughsh/online_policy_adaptation_using_rollout/blob/main/documentation/images/settling_time.png" width="500"/>
</p>

## Running data collection script
To gather data, execute the file located at the following path: src/TNSM2023/data_collection/run_data_collection.py. 

Within this file, you will define the service name intended for operation on the testbed, set the load range, and specify the data collection method (either grid or random search).

Below is the list of input arguments for this file:

* --IP_port: This argument represents the IP address and port of the services operational on the testbed. Multiple ports and IPs can be defined in a list format, such as x.x.x.x:yyyy (not implemented in this file and version).
* --path_to_artifacts: This argument denotes the directory containing all output files.
* --path_to_data_file: Use this argument to specify the filename for storing data.
* --path_to_LG: This argument requires the path to the load generator.
* --path_to_config_files: This argument indicates the path to the .yaml configuration files.
