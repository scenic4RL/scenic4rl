from random import randint

import gfootball
import gym
#from scenic.simulators.gfootball.rl import pfrl_training

from gfootball.env import football_action_set

#Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning
from scenic.simulators.gfootball.utilities import scenic_helper
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario


def basic_training(scenario):
    #settings = scenario.settings

    #env = gfootball.env.create_environment(env_name="11_vs_11_stochastic", stacked=True, representation='extracted', rewards="scoring,checkpoints")
    #env2 = gfootball.env.create_environment(env_name="11_vs_11_stochastic", stacked=True, representation='extracted', rewards="scoring,checkpoints", other_config_options={"action_set":"v2"})
    #run_built_in_ai_game_with_rl_env(env)


    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring,checkpoints',
        "representation" : 'extracted',
        "players" : [f"agent:left_players=1"]
    }

    rl_env = GFScenicEnv(initial_scenario = scenario, gf_env_settings=gf_env_settings)
    run_built_in_ai_game_with_rl_env(rl_env)


def run_built_in_ai_game_with_rl_env(rl_env, trials=3):
    rl_env.render()
    tot_r_arr = []
    for _ in range(trials):
        tot_r = 0

        _ = rl_env.reset()
        #input("Enter to run simulation:\n")
        while True:
            o, r, d, i = rl_env.step([football_action_set.action_shot]) #football_action_set.action_builtin_ai
            tot_r += r
            #print(r, d, i)
            #input("step?")
            if d: break

        tot_r_arr.append(tot_r)

    print(tot_r_arr)





class GFScenicEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, initial_scenario, gf_env_settings = {}, allow_render = False, use_scenic_behavior_in_step=False
                 , constraints_checking=False,  compute_scenic_actions=False): #
        super(GFScenicEnv, self).__init__()

        self.gf_env_settings = gf_env_settings
        self.allow_render = allow_render
        self.scenario = initial_scenario
        self.constraints_checking = constraints_checking
        self.compute_scenic_actions = compute_scenic_actions
        # self.initial_scenario = initial_scenario

        #self.create_new_simulation = True #if set, initialize_new_simulation, will create a new simulation object, otherwise it will just return
        #self.gf_gym_env = None
        #self.initialize_new_simulation(render=allow_render)

        from gym.spaces.discrete import Discrete
        from gym.spaces import Box
        from numpy import uint8

        assert self.gf_env_settings["action_set"] == "default" or use_scenic_behavior_in_step
        assert self.gf_env_settings["representation"]=="extracted"
        assert self.gf_env_settings["stacked"] == True

        if self.gf_env_settings["action_set"] != "default": print("Environment started with action set: ", self.gf_env_settings["action_set"])

        self.observation_space = Box(low=0, high=255, shape=(72, 96, 16), dtype=uint8)
        self.action_space = Discrete(19)

        self.use_scenic_behavior_in_step = use_scenic_behavior_in_step

        if self.use_scenic_behavior_in_step:
            print("Environment will ignore actions passed to step() and take action provided by Scenic")


    def reset(self):

        # Reset the state of the environment to an initial state

        #self.initialize_new_simulation(render=self.allow_render)
        #self.create_new_simulation = True
        self.scene, _ = scenic_helper.generateScene(self.scenario)


        if hasattr(self, "simulation"): self.simulation.get_underlying_gym_env().close()
        from scenic.simulators.gfootball.simulator import GFootBallSimulation
        self.simulation = GFootBallSimulation(scene=self.scene, settings={}, for_gym_env=True,
                                              render=self.allow_render, verbosity=1, gf_env_settings=self.gf_env_settings,
                                              use_scenic_behavior_in_step= self.use_scenic_behavior_in_step,
                                              constraints_checking=self.constraints_checking, compute_scenic_actions=self.compute_scenic_actions)

        self.gf_gym_env = self.simulation.get_underlying_gym_env()

        return self.simulation.reset()

    def set_scecario(self, scenario):
        self.scenario = scenario
        #self.create_new_simulation = True

    def step(self, action):
        # Execute one time step within the environment
        return self.simulation.step(action)

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        #For weird pygame rendering issue, rendering must be called in utilities/env_creator/create_environment
        return None


def test_gfootball_env_wrapper_code():
    env = gfootball.env.create_environment(env="11_vs_11_stochastic", stacked=True, representation='extracted')


def lock_step_test():
    import os
    cwd = os.getcwd()

    scenario_file = f"{cwd}/rl/exp_0_0/academy_empty_goal_close.scenic"
    scenario = buildScenario(scenario_file)

    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring,checkpoints',
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default"
    }

    from scenic.simulators.gfootball.rl_interface import GFScenicEnv
    sce_env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)

    env = gfootball.env.create_environment("academy_empty_goal_close", number_of_left_players_agent_controls=1, render=False,
                                           representation="extracted", stacked=True,
                                           rewards="scoring,checkpoints")



    import numpy as np


    rew = 0
    rew_s = 0
    for _ in range(10):
        o_s = sce_env.reset()
        prev_s = o_s
        o = env.reset()
        #print(o_s.shape, o.shape)
        d_s = False
        d = False
        while True:
            a = randint(0,18)

            if not d_s:
                #print(a)
                o_s, r_s, d_s, i_s  = sce_env.step(a)
                rew_s += i_s["score_reward"]
            if not d:
                o, r, d, i = env.step(a)
                rew += i["score_reward"]


            #print(a, "scenic", np.sum(o_s), r_s, d_s, i_s, "raw", np.sum(o), r, d, i)
            #print((o_s==prev_s).all())
            #print(np.where(o_s[:,:,2]), np.where(o_s[:,:,3])) # active_player, ball
            #print(np.where(o[:, :, 2]), np.where(o[:, :, 3]))
            #print()
            prev_s=o_s
            if d_s and d : break


    print(rew, rew_s)

def test_rl_rith_scenic_behavior():
    import os
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
                    obs = env.reset()
                    num_epi +=1

        return total_r/num_epi


    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring',
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": True,
        "action_set": "v2",#"default"
    }

    from scenic.simulators.gfootball.rl_interface import GFScenicEnv

    num_trials = 2
    scenario_file = f"{cwd}/rl/rl_demo.scenic"
    scenario = buildScenario(scenario_file)

    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False, use_scenic_behavior_in_step=True)
    print("Trials: ", num_trials)
    print("behavior based agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))


    gf_env_settings["action_set"] = "default"
    env = GFScenicEnv(initial_scenario=scenario, allow_render=False, gf_env_settings=gf_env_settings)
    print("random agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))


def test_with_optional_pre_and_post_step():
    import os
    cwd = os.getcwd()

    def mean_reward_random_agent(env, num_trials=1):

        obs = env.reset()
        # env.render()
        num_epi = 0
        total_r = 0
        from tqdm import tqdm
        for i in tqdm(range(0, num_trials)):

            done = False
            # input("Enter")
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
        "action_set": "default",  # "default"
    }

    from scenic.simulators.gfootball.rl_interface import GFScenicEnv

    num_trials = 10
    scenario_file = f"{cwd}/rl/rl_demo.scenic"
    scenario = buildScenario(scenario_file)

    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False, use_scenic_behavior_in_step=True, constraints_checking=True)
    print("Trials: ", num_trials)
    print("behavior based agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))

    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False, use_scenic_behavior_in_step=True, constraints_checking=True)
    print("Trials: ", num_trials)
    print("behavior based agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))

    gf_env_settings["action_set"] = "default"
    env = GFScenicEnv(initial_scenario=scenario, allow_render=False, gf_env_settings=gf_env_settings, constraints_checking=False)
    print("random agent performance: ", mean_reward_random_agent(env, num_trials=num_trials))



if __name__=="__main__":
    #test_gfootball_env_wrapper_code()
    #lock_step_test()

    #test_rl_rith_scenic_behavior()
    test_with_optional_pre_and_post_step()