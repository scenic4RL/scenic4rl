import gfootball
import scenic.syntax.translator as translator
import scenic.core.errors as errors
from gfootball.env import wrappers, observation_preprocessing

"""
1. Read scenic and generate gfootball scenario
2. Create Environment from that gfootballl scenario and return
    ---> the returned environemnt can be used as an environement to be passed to openaigym baselines
"""

"""
examples/gfootball/try.scenic -S -b --verbosity 2
"""

"""
Pixel representation requires rendering and is supported only for players on the left team. [currently it doesnt work]
"""
def create_single_football_env(scenic_file_path, verbosity=0, iprocess=0, representation=None, stacked=False,
                               channel_dimensions=(
                                observation_preprocessing.SMM_WIDTH,
                                observation_preprocessing.SMM_HEIGHT)):
    """

    :param scenic_file_path:
    :param verbosity:
    :param iprocess:
    :param representation: String to define the representation used to build
      the observation. It can be one of the following: 'pixels', 'pixels_gray', 'extracted', 'simple115'/'simple115v2', None -> raw

    :param channel_dimensions: (width, height) tuple that represents the dimensions of
       SMM or pixels representation.
    :return: GFootballEnvironment
    """


    verbosity = 0
    scenario = errors.callBeginningScenicTrace(
        lambda: translator.scenarioFromFile(scenic_file_path)
    )

    simulator = errors.callBeginningScenicTrace(scenario.getSimulator)
    scene, iterations = errors.callBeginningScenicTrace(
        lambda: scenario.generate(verbosity=verbosity)
    )
    simulation = simulator.createSimulation(scene)

    env = simulation.get_environment()

    """Apply representation/observation and stacking wrapper. Code copied from env/__init__.py/_apply_output_wrappers"""
    if representation is not None:
        env = gfootball.env._process_representation_wrappers(env, representation,
                                     channel_dimensions)

    if stacked:
        env = wrappers.FrameStack(env, 4)

    #env = monitor.Monitor(env, logger.get_dir() and os.path.join(logger.get_dir(),
    #                                                             str(iprocess)))
    return env


if __name__=="__main__":
    env = create_single_football_env("/Users/azadsalam/codebase/scenic/examples/gfootball/try.scenic", 0)

    #obs = env.reset()

    for i in range(1,100):
        env.step([9]*6)
