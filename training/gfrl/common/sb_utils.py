from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecTransposeImage
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import gym
#from stable_baselines3.common.monitor import Monitor
from gfrl.common.my_sb.monitor import Monitor

def get_env(scenario_file, gf_env_settings, monitordir, rank=0):
    scenario = buildScenario(scenario_file)
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, rank=rank)
    env = Monitor(env, filename=f"{monitordir}_{rank}", info_keywords=("score_reward",))
    return env

def get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu, monitordir):

    def make_env(scenario_file, gf_env_settings, rank):
        def _init():
            return get_env(scenario_file, gf_env_settings, monitordir, rank)
        return _init


    env = SubprocVecEnv([make_env(scenario_file, gf_env_settings, i) for i in range(num_cpu)])

    return env


def get_dummy_vec_env(num_cpu, monitordir):
    #from stable_baselines3.common.monitor import Monitor
    def make_env(rank):
        def _init():
            env = gym.make("CartPole-v1")
            env = Monitor(env, filename = f"{monitordir}_{rank}")
            return env
        return _init

    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])

    return env




def get_incremental_dirname(path, dirname):
    import os

    name =  lambda path, dirname, x: f"{os.path.join(path, dirname)}_{x}"
    i = 0
    while os.path.exists(name(path, dirname, i)):
        #print(f"/{path}/{dirname}_{i}")
        i += 1

    return name(path, dirname, i)
