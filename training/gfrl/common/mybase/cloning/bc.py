import os
import time
import numpy as np
import os.path as osp
from baselines import logger
from collections import deque
from baselines.common import explained_variance, set_global_seeds
from baselines.common.policies import build_policy
try:
    from mpi4py import MPI
except ImportError:
    MPI = None
from baselines.ppo2.runner import Runner


def constfn(val):
    def f(_):
        return val
    return f

def learn(*, network, env, total_timesteps, dataset=None, eval_env = None, seed=None, nsteps=2048, ent_coef=0.0, lr=3e-4,
            vf_coef=0.5,  max_grad_norm=0.5, gamma=0.99, lam=0.95,
            log_interval=10, nminibatches=4, noptepochs=4, cliprange=0.2,
            save_interval=0, load_path=None, model_fn=None, update_fn=None, init_fn=None, mpi_rank_weight=1, comm=None, eval_interval=1, **network_kwargs):

    set_global_seeds(seed)
    if isinstance(lr, float): lr = constfn(lr)
    else: assert callable(lr)
    if isinstance(cliprange, float): cliprange = constfn(cliprange)
    else: assert callable(cliprange)
    total_timesteps = int(total_timesteps)

    policy = build_policy(env, network, **network_kwargs)

    # Get the nb of env
    nenvs = env.num_envs

    # Get state_space and action_space
    ob_space = env.observation_space
    ac_space = env.action_space

    # Calculate the batch_size
    nbatch = nenvs * nsteps
    nbatch_train = nbatch // nminibatches
    is_mpi_root = (MPI is None or MPI.COMM_WORLD.Get_rank() == 0)

    
    # Instantiate the model object (that creates act_model and train_model)

    from baselines.ppo2.model import Model
    from gfrl.common.mybase.cloning.bc_model import BCModel
    model_fn = BCModel

    model = model_fn(policy=policy, ob_space=ob_space, ac_space=ac_space, nbatch_act=nenvs, nbatch_train=nbatch_train,
                    nsteps=nsteps, ent_coef=ent_coef, vf_coef=vf_coef,
                    max_grad_norm=max_grad_norm, comm=comm, mpi_rank_weight=mpi_rank_weight)

    if load_path is not None:
        model.load(load_path)
    # Instantiate the runner object
    runner = Runner(env=env, model=model, nsteps=nsteps, gamma=gamma, lam=lam)
    if eval_env is not None:
        eval_runner = Runner(env = eval_env, model = model, nsteps = nsteps, gamma = gamma, lam= lam)

    epinfobuf = deque(maxlen=100)
    if eval_env is not None:
        eval_epinfobuf = deque(maxlen=100)

    if init_fn is not None:
        init_fn()

    # Start total timer
    tfirststart = time.perf_counter()

    print("Training BC")

    n_epochs = 30
    nupdates = dataset.num_pairs * n_epochs // nbatch_train
    print(f"Dataset Size: {dataset.num_pairs}")
    print(f"NEpochs: {n_epochs} NUpdates: {nupdates}")

    for update in range(nupdates):
        obs, acts = dataset.get_next_batch(batch_size=nbatch_train)
        loss = model.train_bc(obs=obs, actions=acts, lr=3e-4)
        print(f"step: {update} bc loss: {loss}")


        #if update==nupdates and logger.get_dir() and is_mpi_root:
        if update==nupdates-1 and logger.get_dir():
            checkdir = osp.join(logger.get_dir(), 'checkpoints')
            os.makedirs(checkdir, exist_ok=True)

            if update == nupdates-1: savepath = osp.join(checkdir, 'bc_final_%.5i'%update)
            else: savepath = osp.join(checkdir, 'bc_%.5i'%update)
            print('Saving to', savepath)
            model.save(savepath)

    return model


def safemean(xs):
    return np.nan if len(xs) == 0 else np.mean(xs)


