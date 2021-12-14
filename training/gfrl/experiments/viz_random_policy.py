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


scenario_file = "/home/ek65/Desktop/scenic4rl/training/gfrl/_scenarios/offense/3vs1_offense.scenic"


from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
scenario = buildScenario(scenario_file)

# from scenic.simulators.gfootball.rl.gfScenicEnv_v1 import GFScenicEnv_v1
#env = GFScenicEnv_v1(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True, compute_scenic_behavior=False)

from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2
env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True)
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
        # print(r)
        #input("Press Any Key to Continue")
        #input("Press Any Key to Continue")
    print(tr)