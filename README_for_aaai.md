
# Installation and Usage Guide for: Programmatic Modeling and Generation of Real-time Strategic Soccer Environments for Reinforcement Learning (Paper ID: 2485)

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


In this repository we provide details of our interace, installation guidelines, links to saved checkpoints and training logs, and instructions to reproduce the experiments.




## Installation
### 1. Set up Python3.7 and Poetry
1. Install Python 3.7 
2. Install Poetry. Please refer to:
	https://python-poetry.org/docs/#installation
### 2. Install Google Research Football and Our Interface
3. Download the codebase we shared.
4. Create a virtual environment in `ScenicGFootBall` using `poetry env use python3.7`. Activate it using `poetry shell`.
5. In `ScenicGFootBall` run `poetry install`
	This will install Scenic and Our Interface in editable mode.
6. Install Google Research Football. Please refer to:
	https://github.com/google-research/football#on-your-computer
7. Install RL Training dependencies including Tensorflow 1.15, Sonnet, and OpenAI Baselines. Please refer to:
	https://github.com/google-research/football#run-training
8. Go to the folder `training` and run `python3 -m pip install -e .` to install our  package `gfrl` which we use to conduct the experiments.
### 3. Test the installation by running:
Run the following program to create an environment with a scenic scenario script and running a random agent.

    
    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    scenario = buildScenario("..path to a scenic script..") #Find all our scenarios in training/gfrl/_scenarios/
    
    from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2

    env_settings = {
        "stacked": True,
        "rewards": 'scoring',
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": True
        }
	env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=env_settings)
    
    env.reset()
    done = False

    while not done:
        action = env.action_space.sample()
        _, _, done, _ = env.step(action)

## Dataset of scenarios and probabilistic scenic policies

### Scenarios 
All of our proposed scenarios can be found in the `training/gfrl/_scenarios` directory, categorized according to their type. Proposed Defense and Offense Scenarios are placed in `training/gfrl/_scenarios/defense` and `training/gfrl/_scenarios/offense` directories, respectively. 
Scenic scenario scripts corresponding to select GRF scenarios can be found in `training/gfrl/_scenarios/grf`. `training/gfrl/_scenarios/testing_generalization` contains testing scripts corresponding to all the above mentioned scenarios. 

### Scenic Policies and Demonstration Data
Scenic semi-expert policy scripts for select scenarios can be found in `training/gfrl/_scenarios/demonstration`. Data generated from these policies are placed in `training/gfrl/_demonstration_data`.

## Interface
### Create Environment

First Create Scenic scenario object:

    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario  
    scenario = buildScenario(scenario_file)

Then, Create Gym Environment from Scenic scenario:

*env_type* : We now offer two different environment classes, i.e., `GFScenicEnv_v1` and `GFScenicEnv_v2`. We recommend to use `GFScenicEnv_v2`, which is our default environment implementing all the features and experiments discussed in the paper. `GFScenicEnv_v1` only allows the initial distribution of states, but doesnt allow to use Scenic behaviors for non-RL agents, i.e., it always uses the Default AI behavior provided by GRF for the non-RL agents. 

    from scenic.simulators.gfootball.rl.gfScenicEnv_v1 import GFScenicEnv_v1  
    from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2  
     
    env_type = "... use appropriate env class according to your need..."
    if env_type=="v1":  
       env = GFScenicEnv_v1(initial_scenario=scenario, gf_env_settings=gf_env_settings, compute_scenic_behavior=True)  
    elif env_type=="v2":  
       env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=gf_env_settings)  
    else:  
       assert False, "invalid env_type"

Please refer to `training/gfrl/base/bc/utils.py` for further details.

### Generate Demonstration Data from Scenic Scenario Scripts
For generating expert data using Scenic policies, we need to execute scenic policies at each timestep to generate an action. At any timestep, one can use the environment method `env.simulation.get_scenic_designated_player_action()` to read the action that was computed corresponding to the `active` player. 

We provide helper scripts to automate the process though. One can simply follow the following steps to generate data:  

1. Open `training/gfrl/experiments/gen_demonstration.py`
2. Change the following fields:
	- scenario: Path to the scenic policy scripts
	- data_path: The output file path **without** any extension.

3. Run `python3 training/gfrl/experiments/gen_demonstration.py`

To read the saved offline data, run the following: 


    from gfrl.common.mybase.cloning.dataset import get_datasets
    tds, vds = get_datasets("..path to the saved data...", validation_ratio=0.0)
    
    print("train")
    print(tds.summary())
    print()
    
    print("validation")
    print(vds.summary())
    print()

## Reproducability 


### Run training with PPO

In order to reproduce PPO results from the paper, please refer to:

- training/gfrl/experiments/score_scenic.sh


### Train agents from Demonstration Data using Behavior Cloning
1. Open `training/gfrl/experiments/bc.sh`
2. Change the following fields:
	- level: Path to the scenic scenario scripts
	- eval_level: Should be the same as level
	- dataset: The .npz demonstration data file generated by `gen_demonstration.py`.
	- n_epochs: Change it to 5 for offense and 16 for grf scenarios to reproduce the paper's results
	- exp_root: where to store the training outputs
	- exp_name: output directory's name
3. Run `bash training/gfrl/experiments/bc.sh`
### Train the pretrained-agents (e.g., from behavior cloning)  with PPO
With default settings, the script will train the model for 5M timesteps.
1. Open `training/gfrl/experiments/pretrain.sh`
2. Change the following fields:
	- level: Path to the Scenic scenario scripts
	- eval_level: Should be the same as level
	- exp_root: where to store the training outputs
	- exp_name: output directory's name
	- load_path: path to the behavior cloning model
3. Run `bash training/gfrl/experiments/pretrain.sh`
### Testing for Generalization 
Please use the following script to evaluate the model's mean score.
1. Open `training/gfrl/experiments/test_agent.sh`
2. Change the following fields:
	- eval_level: path to the Scenic scenario scripts
	- load_path: path to the model to be evaluated 
	- write_video: Set it to False
	- dump_full_episodes: Set it to False
3. Run `bash training/gfrl/experiments/test_agent.sh`
4. The result will be printed in the end in the following format:
`exp_name, reward_mean, score_mean, ep_len_mean, num_test_epi, test_total_timesteps, eval_level, load_path`.


### Trained checkpoints
We pubicly share tensorboard log and saved checkpoints for all our experiments [here](https://drive.google.com/drive/folders/11E1odAtLGh6mjoI2q3bkha3ZautX8XOo?usp=sharing).   

## Acknowledgement
We'd like to thank the Scenic and GRF Team for open sourcing their projects.

