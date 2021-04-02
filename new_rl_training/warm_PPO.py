from  common.ppo_util import MyEvalCallback 
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
from scenic.simulators.gfootball import rl_interface
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import gym
from tqdm import tqdm
import numpy as np
import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from stable_baselines3 import PPO, A2C, SAC, TD3
from stable_baselines3.common.evaluation import evaluate_policy

from torch.utils.data.dataset import Dataset, random_split
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os
import datetime
import gym

from typing import Union, List, Dict, Any, Optional
from stable_baselines3.common.vec_env import VecEnv, sync_envs_normalization, DummyVecEnv
import numpy as np
import warnings
from typing import Union

def make_gf_env(rank, scenario_file, seed=0):

    def _init():
        gf_env_settings = {
            "stacked": True,
            "rewards": "scoring",
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False,
            "action_set": "default"
        }
        
        from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
        scenario = buildScenario(scenario_file)

        env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False)
        #env.seed(seed + rank)
        return env

    set_random_seed(seed)
    return _init

if __name__ == "__main__":

    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    scenario_file = f"{cwd}/pretrain/scenarios/pass_n_shoot.scenic"
    pretrained_model = f"{cwd}/pretrain/models/cnn_adam_pass_n_shoot_20000_50"

    n_eval_episodes = 10
    total_training_timesteps = 10000
    eval_freq = 5000
    num_cpu=6

    save_dir = f"{cwd}/pretrain/saved_models"
    logdir = f"{cwd}/pretrain/tboard/pass_n_shoot/"
    tracedir = f"{cwd}/game_trace"
    rewards = "scoring"#'scoring,checkpoints'
    
    print("model, tf logs, game trace are saved in: ", save_dir, logdir, tracedir)


    for sn, pretraining in enumerate([False]):
        
        #env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False)
        env = SubprocVecEnv([make_gf_env(i,scenario_file) for i in range(num_cpu)])
        #env = Monitor(env)
        
        loaded = PPO.load(pretrained_model)

        parameters = dict(clip_range=0.115, gamma=0.997, learning_rate=0.00011879,
                          batch_size=1024, n_epochs=10, ent_coef=0.00155, max_grad_norm=0.76,
                          vf_coef=0.5, gae_lambda=0.95, n_steps = 4096)
        

        model = PPO("CnnPolicy", env, verbose=1)

        if pretraining:
            model.policy = loaded.policy 
            print("Loaded weights from pretrained agent")
        else:
            print("No Pretraining. Starting with Random weight")


        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(logdir, exist_ok=True)

        #eval_callback = MyEvalCallback(model.get_env(), eval_freq=eval_freq, deterministic=True, render=False)

        currentDT = datetime.datetime.now()
        fstr = f"HM_{currentDT.hour}_{currentDT.minute}__DM_{currentDT.day}_{currentDT.month}"
        log_file_name = f"{fstr}"

        print("tboard name", log_file_name)

        #model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name, callback=eval_callback) 
        model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name) 

        model_name = "PPO_nature_cnn_pass_n_shoot"
        if pretraining: model_name += "_warm_start"
        model_name+=f"{sn}"
        model.save(f"{save_dir}/{model_name}_{total_training_timesteps}")
        print("-------------")