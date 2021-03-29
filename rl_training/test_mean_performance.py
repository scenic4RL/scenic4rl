from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario


def mean_reward_test(env, num_trials=1, built_in_ai=False):
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
        "action_set": "v2",#"default"
    }

from scenic.simulators.gfootball.rl_interface import GFScenicEnv

import os
cwd = os.getcwd()

num_trials = 50
num_trials_built_in_ai = 10
scenario_files= [f"{cwd}/exp_0_6/2v2.scenic",
                 f"{cwd}/exp_0_6/2v2_0.scenic",
                 f"{cwd}/exp_0_6/2v2_1.scenic",
                 f"{cwd}/exp_0_6/2v2_2.scenic"]


scenario_files = [
    f"{cwd}/exp_0_6/temp.scenic",
]
print("Trials: ", num_trials)

random_score={}
built_in_ai_score  ={}

for scenario_file in scenario_files:
    scenario = buildScenario(scenario_file)

    gf_env_settings["action_set"] = "v2"
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False, use_scenic_behavior_in_step=True)

    print(scenario_file)
    ai_mean = mean_reward_test(env, num_trials=num_trials_built_in_ai)
    built_in_ai_score[scenario_file] = ai_mean
    print("behavior based agent performance: ",ai_mean)


    gf_env_settings["action_set"] = "default"
    env = GFScenicEnv(initial_scenario=scenario, allow_render=False, gf_env_settings=gf_env_settings)

    random_mean = mean_reward_test(env, num_trials=num_trials)
    random_score[scenario_file] = random_mean
    print("random agent performance: ", random_mean)
    print()

import pprint
print("built in ai")
pprint.pprint(built_in_ai_score)
print("random agent")
pprint.pprint(random_score)