print("Loading Data as Dataset for validation")
path = "/home/ubuntu/ScenicGFootBall/training/gfrl/_data/attack_avoid_pass_shoot.npz"
from gfrl.common.mybase.cloning.dataset import get_datasets
tds, vds = get_datasets(path, validation_ratio=0.0)

print("train")
print(tds.summary())
print()

print("validation")
print(vds.summary())
print()