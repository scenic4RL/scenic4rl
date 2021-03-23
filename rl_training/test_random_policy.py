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
    "dump_full_episodes": True,
    "dump_scores": True,
    "write_video": True,
    "tracesdir": tracedir,
    "write_full_episode_dumps": True,
    "write_goal_dumps": True,
    "render": True
}

scenario_file = f"{cwd}/exp_0_4/academy_run_to_score.scenic"
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(scenario_file)

env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)


for _ in range(2):
    env.reset()

    done = False

    while not done:
        _,_,done,_ = env.step(env.action_space.sample())