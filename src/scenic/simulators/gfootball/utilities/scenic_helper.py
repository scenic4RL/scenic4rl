import time
import scenic.core.errors as errors
import scenic.syntax.translator as translator

"""Copied from __main__.py"""
def generateScene(scenario, verbosity=0, show_params=False):
    startTime = time.time()
    scene, iterations = errors.callBeginningScenicTrace(
        lambda: scenario.generate(verbosity=verbosity)
    )
    if verbosity >= 1:
        totalTime = time.time() - startTime
        print(f'  Generated scene in {iterations} iterations, {totalTime:.4g} seconds.')
        if show_params:
            for param, value in scene.params.items():
                print(f'    Parameter "{param}": {value}')
    return scene, iterations




def buildScenario(scenic_file, param=[], model=None, scenario=None):
    errors.showInternalBacktrace = True
    scenario = errors.callBeginningScenicTrace(
        lambda: translator.scenarioFromFile(scenic_file,
                                            params=param,
                                            model=model,
                                            scenario=scenario)
    )
    return scenario
