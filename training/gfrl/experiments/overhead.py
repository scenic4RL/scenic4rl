import os
cwd = os.getcwd()
import time
time.perf_counter()



env_settings = {
    "stacked": True,
    "rewards": 'scoring',
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True
}

n_interaction = 100
scenarios_scenic = ["/Users/codebase/scenic/training/gfrl/_scenarios/academy/pass_n_shoot.scenic",
					"/Users/codebase/scenic/training/gfrl/_scenarios/academy/run_pass_shoot.scenic"]
scenarios_gf = ["academy_empty_goal", "academy_empty_goal_close", "academy_pass_and_shoot_with_keeper", "academy_run_pass_and_shoot_with_keeper", "academy_run_to_score_with_keeper"]

info = {}

from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2


def run_random_policy(env, n_interaction):
	env.reset()

	for _ in range(n_interaction):
		o, r, d, _ = env.step(env.action_space.sample())

		if d: env.reset()



for scenario_file in scenarios_scenic:

	from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
	scenario = buildScenario(scenario_file)
	env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=env_settings)

	t0 = time.perf_counter()
	run_random_policy(env, n_interaction=n_interaction)
	t1 = time.perf_counter()

	info["scenic_"+scenario_file] = t1-t0

import gfootball.env as football_env

for scenario in scenarios_gf:
	env = football_env.create_environment(
		env_name=scenario,
		stacked=True,
		rewards="scoring"
	)

	t0 = time.perf_counter()
	run_random_policy(env, n_interaction=n_interaction)
	t1 = time.perf_counter()

	info["raw_gf_" + scenario] = t1 - t0




print(info)
with open("overhead.csv", "a+") as f:
	for k,v in info.items():
		f.write(f"{k}, {n_interaction},  {v}\n")





