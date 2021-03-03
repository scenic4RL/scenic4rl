from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import gfootball

from rl_training import train_template
from rl_training.gfootball_impala_cnn import GfootballImpalaCNN

def train(scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, rewards):


    env = gfootball.env.create_environment(scenario_name, number_of_left_players_agent_controls=1, render=False, representation="extracted",
                                                   rewards=rewards, stacked=True)
    features_extractor_class = GfootballImpalaCNN

    train_template.train(env=env, ALGO=PPO, features_extractor_class = features_extractor_class,
          scenario_name=scenario_name, n_eval_episodes=n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, dump_info={"rewards": rewards})



if __name__ == "__main__":
    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    n_eval_episodes = 10
    total_training_timesteps = 2000
    eval_freq = 10000

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard"
    rewards = 'scoring,checkpoints'
    print(save_dir, logdir)

    train(scenario_name="academy_empty_goal_close", n_eval_episodes = n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, rewards=rewards)

