from scenic.simulators.gfootball import rl_interface
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

import os
cwd = os.getcwd()


tracedir = f"vids"
rewards = "scoring"#'scoring,checkpoints'
gen_video = False
dump=False

gf_env_settings = {
    "stacked": True,
    "rewards": rewards,
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True,
    "action_set": "default",
    "dump_full_episodes": dump,
    "dump_scores": dump,
    "write_video": gen_video,
    "tracesdir": tracedir,
    "write_full_episode_dumps": dump,
    "write_goal_dumps": dump,
    "render": gen_video
}


scenario_file = f"/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/offense/wb/ps_3v2_0_wb_0.scenic"

#scenario_file = f"../_scenarios/academy/11v1.scenic"
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(scenario_file)

from scenic.simulators.gfootball.rl.gfScenicEnv_v1 import GFScenicEnv_v1
env = GFScenicEnv_v1(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True, compute_scenic_behavior=True)

from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2
#env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True)
#env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True)


import gfootball

#env = gfootball.env.create_environment("academy_pass_and_shoot_with_keeper", number_of_left_players_agent_controls=1, render=False, representation="extracted",
#                                                   rewards=rewards, stacked=True, write_video=True, write_full_episode_dumps=True, logdir=tracedir)

for _ in range(1):
    env.reset()
    input("Press Any Key to Continue")
    done = False
    tr = 0
    while not done:
        action = env.simulation.get_scenic_designated_player_action()
        _,r,done,_ = env.step(action)
        tr += r
        print(r)
        #input("Press Any Key to Continue")
        #input("Press Any Key to Continue")
    print(tr)