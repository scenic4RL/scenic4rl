import gym
import numpy as np
#from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecTransposeImage
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
import os


def train_ppo(env, eval_env, config):

    params = config["params"]
    os.makedirs(params["tfdir"], exist_ok=True)
    os.makedirs(params["monitor_dir"], exist_ok=True)
    os.makedirs(params["eval_logdir"], exist_ok=True)

    param_filename = os.path.join(params["exp_dir"]+"/params.txt")
    with open(param_filename, "w+") as ff:
        from pprint import pprint
        pprint(config, stream=ff)

    import pickle
    param_filename = os.path.join(params["exp_dir"] + "/params.p")
    with open(param_filename, "wb") as ff:
        pickle.dump(config, ff)


    from gfrl.common.my_sb import my_eval_callback

    eval_callback = my_eval_callback.EvalCallback(eval_env, best_model_save_path=params["eval_logdir"],
                                                  log_path=params["eval_logdir"], eval_freq=params["eval_freq"],
                                                  deterministic=True, render=False, model_save_freq=params["model_save_freq"],
                                                  n_eval_episodes=params["n_eval_episodes"])


    from gfrl.common.my_sb.ppo import PPO

    # n_updates = total_timesteps // (n_steps*num_cpus)
    model = PPO('CnnPolicy', env, verbose=1, n_epochs=params["n_epochs"], n_steps=params["n_steps"], tensorboard_log=params["tfdir"])
    model.learn(total_timesteps=params["total_timesteps"], callback=[eval_callback])

    model.save(os.path.join(params["eval_logdir"], f"final_model"))


def run_ppo_from_scenario(scenario_file, config = {}):

    gf_env_settings = config["gf_env_settings"]
    params = config["params"]
    num_cpu = params["num_cpu"]
    monitor_dir = params["monitor_dir"]

    os.makedirs(params["monitor_dir"], exist_ok=True)


    from gfrl.common import sb_utils
    env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu, monitordir=monitor_dir)
    env = VecTransposeImage(env)

    eval_env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu=1, monitordir=monitor_dir)
    eval_env = VecTransposeImage(eval_env)

    train_ppo(env, eval_env, config)

def dev_run():
    gf_env_settings = {
        "stacked": True,
        "rewards": "scoring",  # "scoring,checkpoints"
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
    scenario_file = f"{cwd}/../_scenarios/exp/pass_n_shoot.scenic"

    exp_dir = sb_utils.get_incremental_dirname(exp_root, exp_name)
    tfdir = exp_dir
    monitor_dir = os.path.join(exp_dir, "monitor/")
    eval_logdir = os.path.join(exp_dir, "eval/")

    num_cpu = 2  # Number of processes to use
    n_epochs = 8
    n_steps = 1024

    eval_freq = 5000 // num_cpu
    n_eval_episodes = 10
    model_save_freq = 5000
    total_timesteps = 10000


    param_dict = dict(num_cpu=num_cpu, n_epochs=n_epochs, n_steps=n_steps, eval_freq=eval_freq, n_eval_episodes=n_eval_episodes,
                      model_save_freq=model_save_freq, total_timesteps=total_timesteps, exp_root=exp_root, exp_name=exp_name,
                      exp_dir = exp_dir, monitor_dir=monitor_dir, tfdir=tfdir, eval_logdir=eval_logdir)

    config = {"params": param_dict, "gf_env_settings": gf_env_settings}

    run_ppo_from_scenario(scenario_file, config=config)

if __name__ == '__main__':

    dev_run()




