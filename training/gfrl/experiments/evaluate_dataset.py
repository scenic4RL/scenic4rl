print("Loading Data as Dataset for validation")
path = "/Users//gdrive_berkeley/sc4rl_data/demonstration_data/offense_11_vs_GK.npz"
from gfrl.common.mybase.cloning.dataset import get_datasets
tds, vds = get_datasets(path, validation_ratio=0.0)

print("train")
print(tds.summary())
print()

print("validation")
print(vds.summary())
print()