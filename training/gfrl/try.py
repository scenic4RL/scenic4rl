import gfootball
import scenic
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import os
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

scenario_file = f"{os.getcwd()}/_scenarios/exp/pass_n_shoot.scenic"

gf_env_settings = {
    "stacked": True,
    "rewards": "scoring",
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": False,
    "action_set": "default",
    "dump_full_episodes": False,
    "dump_scores": False,
    "write_video": False,
    "tracesdir": "dummy",
    "write_full_episode_dumps": False,
    "write_goal_dumps": False,
    "render": False
}

scenario = buildScenario(scenario_file)
env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, rank=0)
n_trials = 10
rews=[]
for _ in range(n_trials):
    done = False
    rew = 0
    o = env.reset()
    while not done:
        action = env.action_space.sample()
        o,r,done,_ = env.step(action)
        rew += r 

    rews.append(rew)

print(rews)