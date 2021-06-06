from scenic.simulators.gfootball import rl_interface
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

import os
cwd = os.getcwd()


tracedir = f"vids"
rewards = "scoring"#'scoring,checkpoints'
"""
gf_env_settings = {
    "stacked": True,
    "rewards": rewards,
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True,
    "action_set": "default",
    "dump_full_episodes": True,
    "dump_scores": True,
    "write_video": True,
    "tracesdir": tracedir,
    "write_full_episode_dumps": True,
    "write_goal_dumps": True,
    "render": True
}
"""
gf_env_settings = {
    "stacked": True,
    "rewards": 'scoring',
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True
}


# scenario_file = f"/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/attack/cross_hard_no_gk.scenic"

scenario_file = f"/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/defense/new_scenarios/with_behavior/test.scenic"

# scenario_file = f"/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/dev/test.scenic"
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(scenario_file)

#env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)

from scenic.simulators.gfootball.rl.gfScenicEnv_v1 import GFScenicEnv_v1
from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2
#env = GFScenicEnv_v1(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True, compute_scenic_behavior=True)

env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False)

import gfootball

#env = gfootball.env.create_environment("academy_pass_and_shoot_with_keeper", number_of_left_players_agent_controls=1, render=False, representation="extracted",
#                                                   rewards=rewards, stacked=True, write_video=True, write_full_episode_dumps=True, logdir=tracedir)
rews =  []

for _ in range(1000):
    env.reset()
    rew = 0
    #input("Press Any Key to Continue")
    done = False

    while not done:
        action = env.action_space.sample()
        #action = env.simulation.get_scenic_designated_player_action()
        _,r,done,_ = env.step(action)
        #input("")
        rew+=r
    print(rew)
    rews.append(rew)

import numpy as np
rews  = np.array(rews)
print("Mean, Count: ", np.mean(rews), rews.shape[0])