import gym
from scenic.simulators.gfootball.simulator import GFootBallSimulation


#Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning
from scenic.simulators.gfootball.utilities import scenic_helper


def basic_training(scenario):
    #settings = scenario.settings
    """
    rl_env = GFootBallSimulation(scene=None, settings = None,
                                 scenario=scenario, is_gym_env=True,
							   render=False, verbosity=1)
    """
    rl_env = GFScenicEnv()



class GFScenicEnv(gym.env):
    metadata = {'render.modes': ['human']}

    def __init__(self, initial_scenario):
        super(GFScenicEnv, self).__init__()

        #self.initial_scenario = initial_scenario
        self.scenario = initial_scenario


        self.gf_gym_env = self.simulation.get_underlying_gym_env()
        # Define action and observation space
        self.action_space = self.gf_gym_env.action_space
        self.observation_space = self.gf_gym_env.observation_space

    def reset(self):
        # Reset the state of the environment to an initial state

        #generate a scene from the current scenario
        self.scene, _ = scenic_helper.generateScene(self.scenario)

        #initialize a new simulation object
        self.simulation = GFootBallSimulation(scene=self.scene, settings=None, for_gym_env=True,
                                              render=False, verbosity=1)

    def set_scecario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        # Execute one time step within the environment
        return self.gf_gym_env.step(action)

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        self.gf_gym_env.render()

