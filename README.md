# Scenic4RL

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Introduction to SC4RL 



## Installation
### 1. Set up Python3.7 and Poetry
1. Install Python 3.7 
2. Install Poetry. Please refer to:
	https://python-poetry.org/docs/#installation
### 2. Install Scenic4RL and Google Research Football
3. Clone this repo.
4. Create a virtual environment in `ScenicGFootBall` using `poetry env use python3.7`. Activate it using `poetry shell`.
5. In `ScenicGFootBall` run `poetry install`
	This will install Scenic in editable mode.
6. Install Google Research Football. Please refer to:
	https://github.com/google-research/football#on-your-computer
7. Install RL Training dependencies including Tensorflow 1.15, Sonnet, and OpenAI Baselines. Please refer to:
	https://github.com/google-research/football#run-training
### 3. Test the installation by running:
	[TODO]


## Dataset

### Scenarios 
All of our proposed scenarios can be found in the `training/gfrl/_scenarios` directory, categorized according to their type. Proposed Offensive and Defensive Scenarios are placed in `training/gfrl/_scenarios/defense` and `training/gfrl/_scenarios/offense` directories, respectively. 
Scenic scenario scripts corresponding to select GRF academy scenarios can be found in `training/gfrl/_scenarios/academy`. `training/gfrl/_scenarios/testing_generalization` contains testing scripts corresponding to all the above mentioned scenarios. 

### Scenic Policy and Demonstration Data
Scenic semi-expert policy scripts for select scenarios can be found in `training/gfrl/_scenarios/demonstration`. Data generated from these policies are placed in `training/gfrl/_demonstration_data`.

## Interface
### Create Environment
### Generate Demonstration Data


## Reproducability 


### Run training with PPO

In order to reproduce PPO results from the paper, please refer to:

- training/gfrl/experiments/score_scenic.sh


### Train agents from demonstration data using Behavior Cloning
...
### Pretraining... 
...
### Testing for Generalization 
...
### Trained checkpoints
...


## Contact Us

Please use our [Mailing List](https://google.com) for communication (comments / suggestions / feature ideas)

To discuss non-public matters directly to the Scenic4RL team, please use scenic4rl@gmail.com.


## Acknowledgement
We'd like to thank the Scenic and GRF Team for open sourcing their projects.

