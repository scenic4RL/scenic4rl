import time
import scenic.core.errors as errors
import scenic.syntax.translator as translator
from scenic.syntax import veneer

"""Copied from __main__.py"""
def generateScene(scenario, maxIterations=2000, verbosity=0, show_params=False):
    startTime = time.time()
    scene, iterations = errors.callBeginningScenicTrace(
        lambda: scenario.generate(maxIterations=maxIterations, verbosity=verbosity)
    )
    if verbosity >= 1:
        totalTime = time.time() - startTime
        print(f'  Generated scene in {iterations} iterations, {totalTime:.4g} seconds.')
        if show_params:
            for param, value in scene.params.items():
                print(f'    Parameter "{param}": {value}')

    scene.name = scenario.name
    scene.scenic_file = scenario.scenic_file
    return scene, iterations




def buildScenario(scenic_file, param=[], model=None, scenario=None):
    veneer.reset()
    errors.showInternalBacktrace = True
    scenario = errors.callBeginningScenicTrace(
        lambda: translator.scenarioFromFile(scenic_file,
                                            params=param,
                                            model=model,
                                            scenario=scenario)
    )

    si = scenic_file.rfind("/") + 1
    ei = scenic_file.rfind(".")
    scenario.name = scenic_file[si:ei]
    scenario.scenic_file = scenic_file

    return scenario
