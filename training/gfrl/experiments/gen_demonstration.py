from gfrl.base.bc.utils import generate_expert_successful_data


scenario = "/Users/azadsalam/codebase/scenic/training/gfrl/_scenarios/offense/wb/fg_11v1_wb.scenic"
num_interactions = 10000
data_path = "/Users/azadsalam/codebase/scenic/training/gfrl/_data/offense_11v1"

expert_observations, acts_oh, expert_rewards = generate_expert_successful_data(scenario_file=scenario, num_interactions=num_interactions, file_name=data_path)
print("#"*80)
print("Data Generation Done")
print("#"*80)

print("Loading Data as Dataset for validation")
from gfrl.common.mybase.cloning.dataset import get_datasets
tds, vds = get_datasets(data_path+".npz", validation_ratio=0.0)

print("train")
print(tds.summary())
print()

print("validation")
print(vds.summary())
print()