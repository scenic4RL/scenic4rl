import verifai
import scenic
from functions import *
from scenic.core.distributions import Samplable, Range
from verifai.samplers.scenic_sampler import *
from scenic.core.utils import DefaultIdentityDict

scenic_file = '/home/ek65/Desktop/VerifAI/2vs2_with_scenic_high_pass_forward.scenic'
scenario = scenic.scenarioFromFile(scenic_file)
objects = scenario.objects

def isInCheckedVar(var, checked_var):
	for v in checked_var:
		if var is v:
			return True
	return False

def randObjParser(obj, subsamples=None, checked_var=[]):
	print("obj: ", obj)
	if subsamples is None:
		subsamples = DefaultIdentityDict()
	for child in obj._conditioned._dependencies:
		if child not in subsamples:
			subsamples[child] = randObjParser(child, subsamples, checked_var)

	var = obj._conditioned
	if isinstance(var, Range) and not isInCheckedVar(var, checked_var):
		checked_var.append(var)
	return obj._conditioned.sampleGiven(subsamples)

randVar_list, checked_var = [], []
sampled_obj = randObjParser(objects[0], checked_var=checked_var)
print(sampled_obj.position)
print("checked_var: ", checked_var)
print(checked_var[0])