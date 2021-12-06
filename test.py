import verifai
import scenic
from functions import *
from scenic.core.distributions import Samplable, Range
from scenic.core.regions import RectangularRegion, PointInRegionDistribution
from scenic.core.vectors import Vector
from verifai.samplers.scenic_sampler import *
from scenic.core.utils import DefaultIdentityDict
import random

def isInCheckedVar(var, checked_var):
	for v in checked_var:
		if var is v:
			return True
	return False

def randObjParser(obj, subsamples=None, checked_var=[]):
	if subsamples is None:
		subsamples = DefaultIdentityDict()
	for child in obj._conditioned._dependencies:
		if child not in subsamples:
			subsamples[child] = randObjParser(child, subsamples, checked_var)

	print("obj: ", obj)
	if isinstance(obj, (Range, PointInRegionDistribution)) and not isInCheckedVar(obj, checked_var):
		print("obj.position: ", obj.region.position)
		print("obj.region.hw: ", obj.region.hw)
		print("obj.region.hl: ", obj.region.hl)
		checked_var.append(obj)
	return obj._conditioned.sampleGiven(subsamples)

# checked_var = []
# sampled_obj = randObjParser(objects[0], checked_var=checked_var)
# print(sampled_obj.position)
# print("checked_var: ", checked_var)
# print(checked_var[0].)

def parseVar(checked_var):
	samplableVars = []
	for var in checked_var:
		if isinstance(var, Range):
			samplableVars.append(tuple([var.low, var.high]))
		elif isinstance(var, PointInRegionDistribution):
			if isinstance(var.region, RectangularRegion):
				region = var.region
				samplableVars.append(tuple([-region.hw, region.hw]))
				samplableVars.append(tuple([-region.hl, region.hl]))
			else:
				raise NotImplementedError
		else:
			raise NotImplementedError
	print("length of samplableVars: ", len(samplableVars))
	return samplableVars

def parseSamplableVars(scenario):
	checked_var = []
	for obj in scenario.objects:
		randObjParser(obj, checked_var=checked_var)
	print("len of checked_var: ", len(checked_var))
	return checked_var

def randomSampleVars(samplableVars):
	sampledVars = []
	for r in samplableVars:
		sampledVars.append(random.uniform(r[0],r[1]))
	return sampledVars

def createInputDictionary(checked_var, sampledVars):
	inputDict = {}
	index = 0
	for var in checked_var:
		if isinstance(var, Range):
			inputDict[var] = sampledVars[index]
			print("sample: ", sampledVars[index])
			index += 1
		elif isinstance(var, PointInRegionDistribution):
			if isinstance(var.region, RectangularRegion):
				region = var.region
				rx = sampledVars[index]
				ry = sampledVars[index+1]
				pt = region.position.offsetRotated(region.heading, Vector(rx, ry))
				inputDict[var] = region.orient(pt)
				print("sample: ", inputDict[var])
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

scenic_file = '/home/ek65/Desktop/scenic4rl/training/gfrl/_scenarios/defense/2vs2_with_scenic_high_pass_forward.scenic'
scenario = scenic.scenarioFromFile(scenic_file)
objects = scenario.objects

samplableVars = parseSamplableVars(scenario)
varRanges = parseVar(samplableVars)
print("varRanges: ", varRanges)

sampledVars = randomSampleVars(varRanges)
print("sampledVars: ", sampledVars)
inputDict = createInputDictionary(samplableVars, sampledVars)

inputVarToScenario(scenario, inputDict)
scene = scenario.generate()

print("scene: ", scene)
for obj in scene[0].objects:
	print("scene position: ", obj.position)

unconditionScenario(scenario)
print("unconditioned")
for obj in scenario.objects:
	print("position: ", obj.position.sample())
print("resample")
for obj in scenario.objects:
	print("position: ", obj.position.sample())