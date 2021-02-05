from scenic.simulators.gfootball.simulator import GFootBallSimulation


#Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning


def basic_training(scenario):
    #settings = scenario.settings
    rl_env = GFootBallSimulation(scene=None, settings = None,
                                 scenario=scenario, is_gym_env=True,
							   render=False, verbosity=1)


