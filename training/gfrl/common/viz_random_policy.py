from scenic.simulators.gfootball import rl_interface
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

import os
cwd = os.getcwd()


tracedir = f"vids"
rewards = "scoring"#'scoring,checkpoints'

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

#scenario_file = f"{cwd}/exp_0_5/academy_pass_and_shoot_with_keeper.scenic"
#scenario_file = f"../_scenarios/generic/rts/gen_0.scenic"
#scenario_file = f"../_scenarios/sc4rl/fg_11v1.scenic"
#scenario_file = f"../_scenarios/sc4rl/fg_5v5.scenic"
scenario_file = f"/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/sc4rl/defense_1vs1_wk_with_rew.scenic"

#scenario_file = f"../_scenarios/academy/11v1.scenic"
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(scenario_file)

from scenic.simulators.gfootball.rl.gfScenicEnv_v1 import GFScenicEnv_v1
from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2


env = GFScenicEnv_v1(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True, compute_scenic_behavior=False)
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
        _,r,done,_ = env.step(env.action_space.sample())
        tr += r
        print(r)
        #input("Press Any Key to Continue")
    print(tr)