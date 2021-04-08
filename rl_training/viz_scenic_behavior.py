from scenic.simulators.gfootball import rl_interface
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import pretrain_template
from gfootball_impala_cnn import GfootballImpalaCNN

import os
cwd = os.getcwd()
cwd = os.getcwd()
print("Current Directory:", cwd)
rewards = "scoring"
save_dir = f"{cwd}/pretrain/saved_models_hp"
logdir = f"{cwd}/tboard/dev/pretrain"
tracedir = f"{cwd}/game_trace"


gf_env_settings = {
        "stacked": True,
        "rewards": "scoring",
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": True,
        "action_set": "default"
    }
target_scenario_name = f"{cwd}/pretrain/pass_n_shoot_wb.scenic"
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(target_scenario_name)
env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True, use_scenic_behavior_in_step=True, constraints_checking=True)


done = False
total_r = 0


for _ in range(25):
    done=False
    obs = env.reset()
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        #env.render()
        total_r+=reward
        if done:
            #num_epi +=1
            pass