import pickle
from utils import Trajectory
from ipynb.fs.full.common import *

def train_nature_ae(proc_obs, latent_dim=64, batch_size = 512, max_epochs = 25, ckpt_path=""):
    import torch
    if ckpt_path=="":
        ckpt_path = f"ae_{latent_dim}_{max_epochs}"
    
    from torch.utils.data import Dataset, DataLoader, RandomSampler, TensorDataset
    
    data = torch.tensor(proc_obs).float()
    dataset = TensorDataset(data)
    sampler = RandomSampler(dataset)
    dataloader = DataLoader(dataset, sampler=sampler, batch_size = batch_size)
    
    ae = NatureAE(flat_dim=2560, latent_dim=latent_dim)
    trainer = pl.Trainer(gpus=0, max_epochs=max_epochs)
    trainer.fit(ae, dataloader)
    trainer.save_checkpoint(ckpt_path)
    
    return trainer


traj_data_path = "rts_rand_traj_1000.pkl"
print("Loading Data...")

trajs = pickle.load(open(traj_data_path,"rb"))
traj_ids, obs_flat, gt_flat, proc_obs = load_data(trajs)

print("Data Loaded") 

batch_size = 512
max_epochs = 25
latent_dim = 8

data_dir = "models"
ckpt_path = f"{data_dir}/nature_ae_{latent_dim}_rts_1000.ckpt"

print("Start Training")
train_nature_ae(proc_obs, latent_dim = latent_dim, max_epochs=max_epochs, ckpt_path=ckpt_path)