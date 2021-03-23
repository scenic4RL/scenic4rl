from scenic.simulators.gfootball import rl_interface
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import train_template
from gfootball_impala_cnn import GfootballImpalaCNN
from stable_baselines3.common.monitor import Monitor

if __name__ == "__main__":
    import os
    cwd = os.getcwd()

    import gym
    env = gym.make('CartPole-v1')
    env = Monitor(env)

    n_eval_episodes = 10
    total_training_timesteps = 500000
    eval_freq = 10000

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard/hp"
    tracedir = f"{cwd}/game_trace"

    log_file_name = "test_cartpole"

    parameters = dict(clip_range=0.08, gamma=0.993, learning_rate=0.0003,
                      batch_size=512, n_epochs=10, ent_coef=0.003, max_grad_norm=0.64,
                      vf_coef=0.5, gae_lambda=0.95, n_steps = 4096)

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir,
                 clip_range=parameters["clip_range"], gamma=parameters["gamma"],
                 learning_rate=parameters["learning_rate"],
                 batch_size=parameters["batch_size"], n_epochs=parameters["n_epochs"], ent_coef=parameters["ent_coef"],
                 max_grad_norm=parameters["max_grad_norm"], vf_coef=parameters["vf_coef"],
                 gae_lambda=parameters["gae_lambda"])

    model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name)