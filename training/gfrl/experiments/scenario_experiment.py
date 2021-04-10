
import os

from gfrl.base.train_PPO import run_ppo_from_scenario

if __name__ == '__main__':

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
    exp_root = f"{cwd}/../_res/"

    num_cpu = 2  # Number of processes to use
    n_epochs = 8
    n_steps = 1024

    eval_freq = 5000 // num_cpu
    n_eval_episodes = 10
    model_save_freq = 5000
    total_timesteps = 10000



    scenario_file = f"{cwd}/../_scenarios/exp/pass_n_shoot.scenic"
    exp_name = scenario_file[scenario_file.rfind("/")+1:scenario_file.rfind(".")]

    exp_dir = sb_utils.get_incremental_dirname(exp_root, exp_name)
    tfdir = exp_dir
    monitor_dir = os.path.join(exp_dir, "monitor/")
    eval_logdir = os.path.join(exp_dir, "eval/")



    param_dict = dict(num_cpu=num_cpu, n_epochs=n_epochs, n_steps=n_steps, eval_freq=eval_freq,
                      n_eval_episodes=n_eval_episodes,
                      model_save_freq=model_save_freq, total_timesteps=total_timesteps, exp_root=exp_root,
                      exp_name=exp_name,
                      exp_dir=exp_dir, monitor_dir=monitor_dir, tfdir=tfdir, eval_logdir=eval_logdir)

    config = {"params": param_dict, "gf_env_settings": gf_env_settings}

    run_ppo_from_scenario(scenario_file, config=config)
