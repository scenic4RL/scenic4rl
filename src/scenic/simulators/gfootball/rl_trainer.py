import gfootball
import gym
#from scenic.simulators.gfootball.rl import pfrl_training

from gfootball.env import football_action_set

#Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning
from scenic.simulators.gfootball.utilities import scenic_helper


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
    #run_built_in_ai_game_with_rl_env(rl_env)
    #pfrl_training.pfrl_training(rl_env)





def run_built_in_ai_game_with_rl_env(rl_env, trials=3):
    rl_env.render()

    for _ in range(trials):

        _ = rl_env.reset()
        #input("Enter to run simulation:\n")
        while True:
            o, r, d, i = rl_env.step([football_action_set.action_shot]) #football_action_set.action_builtin_ai
            #print(r, d, i)
            #input("step?")
            if d: break


class GFScenicEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, initial_scenario, gf_env_settings = {}, allow_render = False):
        super(GFScenicEnv, self).__init__()

        self.gf_env_settings = gf_env_settings
        self.allow_render = allow_render
        self.scenario = initial_scenario
        # self.initial_scenario = initial_scenario

        #self.create_new_simulation = True #if set, initialize_new_simulation, will create a new simulation object, otherwise it will just return
        #self.gf_gym_env = None
        #self.initialize_new_simulation(render=allow_render)

        from gym.spaces.discrete import Discrete
        from gym.spaces import Box
        from numpy import uint8

        assert self.gf_env_settings["action_set"] == "default"
        assert self.gf_env_settings["representation"]=="extracted"
        assert self.gf_env_settings["stacked"] == True

        self.observation_space = Box(low=0, high=255, shape=(72, 96, 16), dtype=uint8)
        self.action_space = Discrete(19)



    """
    def initialize_new_simulation(self, render=False):


        #    del self.gf_gym_env
        #    self.gf_gym_env = None
        #TODO: Why using create_new_simulation ??? - IF Omitted it doesnt even work!!!!
        if not self.create_new_simulation:
            return

        #if self.gf_gym_env is not None:
        #    self.gf_gym_env.close()
        # generate a scene from the current scenario
        self.scene, _ = scenic_helper.generateScene(self.scenario)

        # initialize a new simulation object
        self.simulation = GFootBallSimulation(scene=self.scene, settings={}, for_gym_env=True,
                                              render=render, verbosity=1, gf_env_settings=self.gf_env_settings)

        self.gf_gym_env = self.simulation.get_underlying_gym_env()
        # Define action and observation space
        self.action_space = self.gf_gym_env.action_space
        self.observation_space = self.gf_gym_env.observation_space

        self.create_new_simulation = False


        #try:
        #    self.gf_gym_env.render()
        #except Exception as e:
        #    print(e)
    """

    def reset(self):
        # Reset the state of the environment to an initial state

        #self.initialize_new_simulation(render=self.allow_render)
        #self.create_new_simulation = True
        self.scene, _ = scenic_helper.generateScene(self.scenario)


        if hasattr(self, "simulation"): self.simulation.get_underlying_gym_env().close()
        from scenic.simulators.gfootball.simulator import GFootBallSimulation
        self.simulation = GFootBallSimulation(scene=self.scene, settings={}, for_gym_env=True,
                                              render=self.allow_render, verbosity=1, gf_env_settings=self.gf_env_settings)

        self.gf_gym_env = self.simulation.get_underlying_gym_env()
        # Define action and observation space
        #self.action_space = self.gf_gym_env.action_space
        #self.observation_space = self.gf_gym_env.observation_space
        #print(id(self.scene), id(self.simulation), id(self.gf_gym_env))

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


if __name__=="__main__":
    test_gfootball_env_wrapper_code()