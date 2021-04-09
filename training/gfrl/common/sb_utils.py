from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

def get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu):

    def make_env(scenario_file, gf_env_settings):
        
        def _init():
            scenario = buildScenario(scenario_file)
            env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
            
            return env
        return _init


    env = SubprocVecEnv([make_env(scenario_file, gf_env_settings) for i in range(num_cpu)])

    return env