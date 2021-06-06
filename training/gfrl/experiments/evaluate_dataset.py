print("Loading Data as Dataset for validation")
path = "/Users/azadsalam/codebase/scenic/training/gfrl/_data/prev/sc4rl_fg11v1_rns_rand1_succ_10000.npz"
from gfrl.common.mybase.cloning.dataset import get_datasets
tds, vds = get_datasets(path, validation_ratio=0.0)

print("train")
print(tds.summary())
print()

print("validation")
print(vds.summary())
print()