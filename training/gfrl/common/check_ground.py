import os
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario


gf_env_settings = {
    "stacked": True,
    "rewards": "scoring",
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True,
    "action_set": "default",
    "dump_full_episodes": False,
    "dump_scores": False,
    "write_video": False,
    "tracesdir": "dummy",
    "write_full_episode_dumps": False,
    "write_goal_dumps": False,
    "render": False,
}

scenario_file = f"{os.getcwd()}/../_scenarios/academy/rts_with_keeper.scenic"

scenario = buildScenario(scenario_file)
env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)


n_trials = 2
rews = []
trajs = []

for _ in range(n_trials):
    done = False
    tot_r = 0
    o = env.reset()
    states = []
    states.append(env.simulation.last_raw_obs)
    while not done:
        action = env.action_space.sample()
        o, r, done, _ = env.step(action)
        tot_r += r
        states.append(env.simulation.last_raw_obs)

    rews.append(tot_r)
    trajs.append(states)


print()