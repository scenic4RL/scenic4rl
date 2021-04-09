import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
import os



if __name__ == '__main__':


    gf_env_settings = {
        "stacked": True,
        "rewards": "scoring",
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default",
        "dump_full_episodes": False,
        "dump_scores": False,
        "write_video": False,
        "tracesdir": "dummy", 
        "write_full_episode_dumps": False,
        "write_goal_dumps": False,
        "render": False
    }

    cwd = os.getcwd()
    scenario_file = f"{cwd}/../_scenarios/exp/pass_n_shoot.scenic"
    print(os.getcwd())
    print(scenario_file)
    num_cpu = 4  # Number of processes to use

    from gfrl.common import sb_utils

    env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu)

    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you:
    # env = make_vec_env(env_id, n_envs=num_cpu, seed=0)

    model = PPO('CnnPolicy', env, verbose=1)
    model.learn(total_timesteps=10000)

