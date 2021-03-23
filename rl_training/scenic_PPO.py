from scenic.simulators.gfootball import rl_interface
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import train_template
from gfootball_impala_cnn import GfootballImpalaCNN


def train(scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, tracedir, rewards, override_params={}):
    gf_env_settings = {
        "stacked": True,
        "rewards": rewards,
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default",
        "dump_full_episodes": True,
        "dump_scores": False,
        "write_video": True,
        "tracesdir": tracedir, 
        "write_full_episode_dumps": True,
        "write_goal_dumps": True,
        "render": True
    }
    #write_full_episode_dumps maybe redundant

    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    scenario = buildScenario(scenario_file)

    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
    features_extractor_class = GfootballImpalaCNN

    #rl_interface.run_built_in_ai_game_with_rl_env(env, trials=50)


    train_template.train(env=env, ALGO=PPO, features_extractor_class = features_extractor_class,
          scenario_name=scenario_name, n_eval_episodes=n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, dump_info={"rewards": rewards}, override_params=override_params)


if __name__ == "__main__":

    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)


    scenario_file = f"{cwd}/exp_0_3/academy_run_pass_and_shoot_with_keeper.scenic"
    n_eval_episodes = 10
    total_training_timesteps = 5000000
    eval_freq = 10000

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard/saved"
    tracedir = f"{cwd}/game_trace"
    rewards = "scoring"#'scoring,checkpoints'
    
    print("model, tf logs, game trace are saved in: ", save_dir, logdir, tracedir)

    override_params = {"n_steps": 4096}
    train(scenario_name=scenario_file, n_eval_episodes = n_eval_episodes,
                    total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
                    save_dir=save_dir, logdir=logdir, tracedir=tracedir, rewards=rewards, override_params=override_params)

    """
    #for HT
    for batch_size in [512, 1024]:
        for n_epochs in [10, 25]:
            for n_steps in [2048, 4096]:    

                params = dict(batch_size=batch_size, n_epochs=n_epochs, n_steps=n_steps)

                train(scenario_name=scenario_file, n_eval_episodes = n_eval_episodes,
                    total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
                    save_dir=save_dir, logdir=logdir, tracedir=tracedir, rewards=rewards, override_params=params)

    """