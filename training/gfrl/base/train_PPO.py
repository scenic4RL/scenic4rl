import gym
import numpy as np
#from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecTransposeImage
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
import os



if __name__ == '__main__':

    gf_env_settings = {
        "stacked": True,
        "rewards": "scoring", #"scoring,checkpoints"
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

    from gfrl.common import sb_utils

    cwd = os.getcwd()
    exp_root = f"{cwd}/../_exp/"
    exp_name = "dev"
    exp_dir = sb_utils.get_incremental_dirname(exp_root, exp_name)
    tfdir = exp_dir
    monitor_dir = os.path.join(exp_dir, "monitor/")
    eval_logdir = os.path.join(exp_dir, "eval/")


    scenario_file = f"{cwd}/../_scenarios/exp/pass_n_shoot.scenic"

    os.makedirs(tfdir, exist_ok=True)
    os.makedirs(monitor_dir, exist_ok=True)
    os.makedirs(eval_logdir, exist_ok=True)

    num_cpu = 8  # Number of processes to use
    n_epochs = 8
    n_steps = 1024

    eval_freq = 20000
    n_eval_episodes = 10
    model_save_freq =  100000
    total_timesteps = 1000000


    from gfrl.common import sb_utils

    env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu, monitordir=monitor_dir)
    env = VecTransposeImage(env)

    eval_env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu=1, monitordir=monitor_dir)
    eval_env = VecTransposeImage(eval_env)

    #env = sb_utils.get_dummy_vec_env(num_cpu, monitordir=monitor_dir)
    #eval_env = sb_utils.get_dummy_vec_env(1, monitordir=monitor_dir)

    from gfrl.common.my_sb import my_eval_callback

    eval_callback = my_eval_callback.EvalCallback(eval_env, best_model_save_path=eval_logdir,
                                 log_path=eval_logdir, eval_freq=eval_freq,
                                 deterministic=True, render=False, model_save_freq=model_save_freq, n_eval_episodes = n_eval_episodes)


    #eval_callback = my_eval_callback.EvalCallback(eval_env, eval_freq=500,deterministic=True, render=False)

    from gfrl.common.my_sb.ppo import PPO

    #n_updates = total_timesteps // (n_steps*num_cpus)
    model = PPO('CnnPolicy', env, verbose=1, n_epochs=n_epochs, n_steps=n_steps, tensorboard_log=tfdir)
    model.learn(total_timesteps=total_timesteps, callback=[eval_callback])

    model.save(os.path.join(eval_logdir, f"final_model"))



