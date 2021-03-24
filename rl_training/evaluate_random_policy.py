from scenic.simulators.gfootball import rl_interface
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import train_template
from gfootball_impala_cnn import GfootballImpalaCNN

import os
cwd = os.getcwd()


tracedir = f"vids"
rewards = "scoring"#'scoring,checkpoints'

gf_env_settings = {
    "stacked": True,
    "rewards": rewards,
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": False,
    "action_set": "default",
    "dump_full_episodes": False,
    "dump_scores": False,
    "write_video": False,
    "tracesdir": tracedir,
    "write_full_episode_dumps": False,
    "write_goal_dumps": False,
    "render": False
}

scenario_file = f"{cwd}/exp_0_5/academy_pass_and_shoot_with_keeper.scenic"
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(scenario_file)

env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)

trials = 50
all_rews = []
for _ in range(trials):
    env.reset()

    rew = 0
    done = False

    while not done:
        _,r,done,_ = env.step(env.action_space.sample())
        rew+=r

    print(rew)
    all_rews.append(rew)


import numpy as np
all_rews=np.array(all_rews)
print("reward", rewards)
print(f"Scenario", scenario_file)
total_r =  np.sum(all_rews)
mean_r = total_r/trials
pos = np.where(all_rews==1)[0].shape[0]
print(f"Mean reward: ", mean_r)
print(f"{pos} times reward was >=1")

with open("random_policy_performance.txt", "a+") as f:
    f.write(f"{mean_r}, {pos}, {trials}, {total_r}, {rewards}, {scenario_file}\n")
