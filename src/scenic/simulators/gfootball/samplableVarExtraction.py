import verifai
import scenic
from scenic.simulators.gfootball.functions import *
from scenic.core.distributions import Samplable, Range, Constant
from scenic.core.regions import RectangularRegion, PointInRegionDistribution
from scenic.core.vectors import Vector
from verifai.samplers.scenic_sampler import *
from scenic.core.utils import DefaultIdentityDict
import random

def issamplableVar(var, samplableVars):
	for v in samplableVars:
		if var is v:
			return True
	return False

def randObjParser(obj, subsamples=None, samplableVars=[]):
	if subsamples is None:
		subsamples = DefaultIdentityDict()
	for child in obj._conditioned._dependencies:
		if child not in subsamples:
			subsamples[child] = randObjParser(child, subsamples, samplableVars)

	# print("obj: ", obj)
	if isinstance(obj, (Range, PointInRegionDistribution)) and not issamplableVar(obj, samplableVars):
		# print("obj.position: ", obj.region.position)
		# print("obj.region.hw: ", obj.region.hw)
		# print("obj.region.hl: ", obj.region.hl)
		samplableVars.append(obj)
	return obj._conditioned.sampleGiven(subsamples)

def parseVar(samplableVars):
	low_high_ranges = []
	for var in samplableVars:
		if isinstance(var, Range):
			low_high_ranges.append(tuple([var.low, var.high]))
		elif isinstance(var, PointInRegionDistribution):
			if isinstance(var.region, RectangularRegion):
				region = var.region
				low_high_ranges.append(tuple([-region.hw, region.hw]))
				low_high_ranges.append(tuple([-region.hl, region.hl]))
			else:
				raise NotImplementedError
		else:
			raise NotImplementedError
	# print("length of samplableVars: ", len(low_high_ranges))
	return low_high_ranges

def low_high_ranges(ranges):
	low, high = [], []
	for elem in ranges:
		low.append(elem[0])
		high.append(elem[1])
	return low, high

def parseSamplableVars(scenario):
	samplableVars = []
	for obj in scenario.objects:
		randObjParser(obj, samplableVars=samplableVars)
	# print("len of checked_var: ", len(checked_var))
	return samplableVars

def randomSampleVars(samplableVars):
	sampledVars = []
	for r in samplableVars:
		sampledVars.append(random.uniform(r[0],r[1]))
	return sampledVars

def createInputDictionary(samplableVars, sampledVars):
	inputDict = {}
	index = 0
	for var in samplableVars:
		if isinstance(var, Range):
			inputDict[var] = Constant(sampledVars[index])
			# print("sample: ", inputDict[var])
			# print("sample._dependencies: ", inputDict[var]._dependencies)
			index += 1
		elif isinstance(var, PointInRegionDistribution):
			if isinstance(var.region, RectangularRegion):
				region = var.region
				rx = sampledVars[index]
				ry = sampledVars[index+1]
				pt = region.position.offsetRotated(region.heading, Vector(rx, ry))
				inputDict[var] = region.orient(pt)
				# print("sample: ", inputDict[var])
				index += 2
			else: 
				raise NotImplementedError
		else:
			raise NotImplementedError
	return inputDict


def conditionInputVar(obj, inputDict, subsamples=None):
	if subsamples is None:
		subsamples = DefaultIdentityDict()

	for child in obj._conditioned._dependencies:
		if child not in subsamples:
			subsamples[child] = conditionInputVar(child, inputDict, subsamples)

	if isinstance(obj._conditioned, (Range, PointInRegionDistribution)) and obj in inputDict.keys():
		# print("obj.position: ", obj.region.position)
		# print("obj.region.hw: ", obj.region.hw)
		# print("obj.region.hl: ", obj.region.hl)
		# if isinstance(obj._conditioned, Range):
		# 	print("Range inputDict[obj]: ", inputDict[obj])
		# 	print("inputDict[obj]._dependencies: ", inputDict[obj]._dependencies)
		obj._conditioned = inputDict[obj]

	return 0

def uncondition(obj, subsamples=None):
	if subsamples is None:
		subsamples = DefaultIdentityDict()

	for child in obj._conditioned._dependencies:
		if child not in subsamples:
			subsamples[child] = uncondition(child, subsamples)

	obj._conditioned = obj
	return 0

def unconditionScenario(scenario):
	for obj in scenario.objects:
		uncondition(obj)

def inputVarToScenario(scenario, inputDict):
	for obj in scenario.objects:
		conditionInputVar(obj, inputDict)
	return None

# scenic_file = '/home/ek65/Desktop/scenic4rl/training/gfrl/_scenarios/defense/2vs2_with_scenic_high_pass_forward.scenic'
# scenario = scenic.scenarioFromFile(scenic_file)

# samplableVars = parseSamplableVars(scenario)
# varRanges = parseVar(samplableVars)
# print("varRanges: ", varRanges)

# sampledVars = randomSampleVars(varRanges)
# print("sampledVars: ", sampledVars)
# inputDict = createInputDictionary(samplableVars, sampledVars)

# inputVarToScenario(scenario, inputDict)
# scene = scenario.generate()

# print("scene: ", scene)
# for obj in scene[0].objects:
# 	print("scene position: ", obj.position)

# unconditionScenario(scenario)
# print("unconditioned")
# for obj in scenario.objects:
# 	print("position: ", obj.position.sample())
# print("resample")
# for obj in scenario.objects:
# 	print("position: ", obj.position.sample())