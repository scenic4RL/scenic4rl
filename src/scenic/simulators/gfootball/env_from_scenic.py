import scenic.syntax.translator as translator
import scenic.core.errors as errors

"""
1. Read scenic and generate gfootball scenario
2. Create Environment from that gfootballl scenario and return
    ---> the returned environemnt can be used as an environement to be passed to openaigym baselines
"""

"""
examples/gfootball/try.scenic -S -b --verbosity 2
"""


def create_single_football_env(scenic_file_path, verbosity, iprocess=0):


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
    #env = monitor.Monitor(env, logger.get_dir() and os.path.join(logger.get_dir(),
    #                                                             str(iprocess)))
    return env


if __name__=="__main__":
    env = create_single_football_env("/Users/azadsalam/codebase/scenic/examples/gfootball/try.scenic", 0)

    #obs = env.reset()

    for i in range(1,100):
        env.step([9]*6)
