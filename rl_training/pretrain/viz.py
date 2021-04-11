import os

from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

cwd = os.getcwd()

def mean_reward_random_agent(env, num_trials=1):

    obs = env.reset()
    #env.render()
    num_epi = 0
    total_r = 0
    from tqdm import tqdm
    for i in tqdm(range(0, num_trials)):

        done = False
        #input("Enter")
        while not done:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            #env.render()
            total_r+=reward
            if done:
                num_epi +=1

                obs = env.reset()

    return total_r/num_epi


gf_env_settings = {
    "stacked": True,
    "rewards": 'scoring',
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": True,
    "action_set": "default",#"default"
}

from scenic.simulators.gfootball.rl_interface import GFScenicEnv

num_trials = 20
scenario_file = f"{cwd}/run_to_score_with_behave.scenic"
scenario = buildScenario(scenario_file)

env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False, use_scenic_behavior_in_step=True)
print("Trials: ", num_trials)
print("behavior based agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))