from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

scenario = buildScenario("/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/academy/empty_goal.scenic")

from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2

env_settings = {
	"stacked": True,
	"rewards": 'scoring',
	"representation": 'extracted',
	"players": [f"agent:left_players=1"],
	"real_time": True
}
env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=env_settings)

env.reset()
done = False

while not done:
	action = env.action_space.sample()
	_, _, done, _ = env.step(action)