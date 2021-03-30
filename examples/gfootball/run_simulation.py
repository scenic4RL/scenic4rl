import os
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
cwd = os.getcwd()

def mean_reward_random_agent(env, num_trials=1):
    obs = env.reset()
    # env.render()
    num_epi = 0
    total_r = 0
    from tqdm import tqdm
    for i in tqdm(range(0, num_trials)):
        done = False
        while not done:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            # env.render()
            total_r += reward
            if done:
                obs = env.reset()
                num_epi += 1

    return total_r / num_epi

gf_env_settings = {
    "stacked": True,
    "rewards": 'scoring',
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True,
    "action_set": "v2",  # "default/v2"
}
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
num_trials = 2
VISUAL = False
scenario_file = f"{cwd}/../../examples/gfootball/try.scenic"
scenario = buildScenario(scenario_file)
env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=VISUAL,
                  use_scenic_behavior_in_step=True)

print("Trials: ", num_trials)
print("behavior based agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))
gf_env_settings["action_set"] = "default"
env = GFScenicEnv(initial_scenario=scenario, allow_render=False, gf_env_settings=gf_env_settings)
print("random agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))