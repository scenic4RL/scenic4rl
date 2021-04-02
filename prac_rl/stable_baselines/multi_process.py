import gym
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = gym.make(env_id)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init


def make_gf_env(rank, seed=0):

    def _init():
        gf_env_settings = {
            "stacked": True,
            "rewards": "scoring",
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False,
            "action_set": "default"
        }
        target_scenario_name = f"pass_n_shoot.scenic"
        from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
        scenario = buildScenario(target_scenario_name)

        env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False)
        #env.seed(seed + rank)
        return env

    set_random_seed(seed)
    return _init



if __name__ == '__main__':
    env_id = "CartPole-v1"
    num_cpu = 4  # Number of processes to use
    # Create the vectorized environment
    #env = SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)])

    env = SubprocVecEnv([make_gf_env(i) for i in range(num_cpu)])


    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you:
    # env = make_vec_env(env_id, n_envs=num_cpu, seed=0)

    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=25000)

    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        #env.render()