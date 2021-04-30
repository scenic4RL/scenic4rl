#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Runs football_env on OpenAI's ppo2."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import multiprocessing
import os
from absl import app
from absl import flags
from baselines import logger
#from baselines.bench import monitor
from gfrl.common.mybase import monitor

from baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
#from baselines.ppo2 import ppo2
import gfootball.env as football_env
from gfootball.examples import models

FLAGS = flags.FLAGS

flags.DEFINE_string('level', '/home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/academy/pass_n_shoot.scenic',
                    'Defines type of problem being solved')
flags.DEFINE_string('eval_level', '/home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/academy/pass_n_shoot.scenic',
                    'Defines type of problem being solved')
flags.DEFINE_enum('state', 'extracted_stacked', ['extracted',
                  'extracted_stacked'],
                  'Observation to be used for training.')

flags.DEFINE_enum('reward_experiment', 'scoring', ['scoring',
                  'scoring,checkpoints'],
                  'Reward to be used for training.')
flags.DEFINE_enum('policy', 'gfootball_impala_cnn', ['cnn', 'lstm', 'mlp', 'impala_cnn',
                  'gfootball_impala_cnn'], 'Policy architecture')

flags.DEFINE_integer('num_envs', 1,
                     'Number of environments to run in parallel.')


flags.DEFINE_integer('num_timesteps', int(2e6),
                     'Number of timesteps to run for.')
flags.DEFINE_integer('nsteps', 128,
                     'Number of environment steps per epoch; batch size is nsteps * nenv'
                     )
flags.DEFINE_integer('noptepochs', 4, 'Number of updates per epoch.')
flags.DEFINE_integer('nminibatches', 8,
                     'Number of minibatches to split one epoch to.')
flags.DEFINE_integer('save_interval', 100,
                     'How frequently checkpoints are saved.')
flags.DEFINE_integer('seed', -1, 'Random seed.')
flags.DEFINE_float('lr', 0.00008, 'Learning rate')
flags.DEFINE_float('ent_coef', 0.01, 'Entropy coeficient')
flags.DEFINE_float('gamma', 0.993, 'Discount factor')
flags.DEFINE_float('cliprange', 0.27, 'Clip range')
flags.DEFINE_float('max_grad_norm', 0.5, 'Max gradient norm (clipping)')
flags.DEFINE_bool('render', False,
                  'If True, environment rendering is enabled.')
flags.DEFINE_bool('dump_full_episodes', False,
                  'If True, trace is dumped after every episode.')
flags.DEFINE_bool('dump_scores', False,
                  'If True, sampled traces after scoring are dumped.')
flags.DEFINE_string('load_path', None,
                    'Path to load initial checkpoint from.')
flags.DEFINE_string('exp_root', "/logs_ppo_gfootball/",
                    'Path to save logfiles, tb, and models.')
flags.DEFINE_string('exp_name', "dev",
                    'Name of Experiment')
flags.DEFINE_integer('eval_interval', 1,
                     'does evaluation after each eval_interval updates'
                     )
flags.DEFINE_integer('eval_timesteps', 400,
                     'How many timesteps for evaluation'
                     )
flags.DEFINE_string('dataset', "/home/ubuntu/ScenicGFootBall/training/gfrl/_data/pns_50.npz",
                     'Path to Dataset'
                     )                    
flags.DEFINE_integer('n_epochs', 2,
                     'Number of epochs'
                     )
flags.DEFINE_integer('batch_size', 32,
                     'Batch Size'
                     )

flags.DEFINE_float('validation_ratio', 0.2,
                     'Portion Kept for Validation'
                     )
                     
flags.DEFINE_bool('run_raw_gf', False,
                  'If True, Raw GFootball Environment will be used.')


def learn(env, policy_func, dataset, optim_batch_size=128, max_iters=1e4,
          adam_epsilon=1e-5, optim_stepsize=3e-4,
          ckpt_dir=None, log_dir=None, task_name=None,
          verbose=False):

    val_per_iter = int(max_iters/10)
    ob_space = env.observation_space
    ac_space = env.action_space

    from baselines.common.policies import build_policy
    network = "gfootball_impala_cnn"
    #Check Network parameters
    network_kwargs = {}
    policy_func = build_policy(env, network, **network_kwargs)

    #pi = policy_func("pi", ob_space, ac_space)  # Construct network for new policy
    # placeholder

    pi = policy_func()
    #print(pi.ac)
    var_list = pi.get_trainable_variables()


    ob = U.get_placeholder_cached(name="ob")
    ac = pi.pdtype.sample_placeholder([None])
    stochastic = U.get_placeholder_cached(name="stochastic")
    loss = tf.reduce_mean(tf.square(ac-pi.ac))
    var_list = pi.get_trainable_variables()
    adam = MpiAdam(var_list, epsilon=adam_epsilon)
    lossandgrad = U.function([ob, ac, stochastic], [loss]+[U.flatgrad(loss, var_list)])

    U.initialize()
    adam.sync()
    logger.log("Pretraining with Behavior Cloning...")
    for iter_so_far in tqdm(range(int(max_iters))):
        ob_expert, ac_expert = dataset.get_next_batch(optim_batch_size, 'train')
        train_loss, g = lossandgrad(ob_expert, ac_expert, True)
        adam.update(g, optim_stepsize)
        if verbose and iter_so_far % val_per_iter == 0:
            ob_expert, ac_expert = dataset.get_next_batch(-1, 'val')
            val_loss, _ = lossandgrad(ob_expert, ac_expert, True)
            logger.log("Training loss: {}, Validation loss: {}".format(train_loss, val_loss))

    if ckpt_dir is None:
        savedir_fname = tempfile.TemporaryDirectory().name
    else:
        savedir_fname = osp.join(ckpt_dir, task_name)
    U.save_variables(savedir_fname, variables=pi.get_variables())
    return savedir_fname


def get_task_name(args):
    task_name = 'BC'
    task_name += '.{}'.format(args.env_id.split("-")[0])
    task_name += '.traj_limitation_{}'.format(args.traj_limitation)
    task_name += ".seed_{}".format(args.seed)
    return task_name

import numpy as np
    

def create_single_scenic_environment(iprocess, level):
    """Creates scenic gfootball environment."""
    from scenic.simulators.gfootball.rl_interface import GFScenicEnv
    import os
    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

    #scenario_file = f"{os.getcwd()}/_scenarios/exp/pass_n_shoot.scenic"
    scenario_file = level
    print("Scenic Environment: ", scenario_file)

    gf_env_settings = {
        "stacked": True,
        "rewards": "scoring",
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default",
        "dump_full_episodes": False,
        "dump_scores": False,
        "write_video": False,
        "tracesdir": "dummy",
        "write_full_episode_dumps": False,
        "write_goal_dumps": False,
        "render": False
    }

    scenario = buildScenario(scenario_file)
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, rank=iprocess)
    env = monitor.Monitor(env, logger.get_dir() and os.path.join(logger.get_dir(), str(iprocess)), info_keywords=("score_reward",))
    return env


def configure_logger(log_path, **kwargs):
    if log_path is not None:
        logger.configure(log_path)
    else:
        logger.configure(**kwargs)    

def train(_):

    #seed = FLAGS.seed
    if FLAGS.seed == -1:
        import random
        import time
        FLAGS.seed = int(time.time())%1000

    
    print("Using Seed: ", FLAGS.seed)
    #quit()
    

    from gfrl.common.mybase.cloning.dataset import GFDset        
    dataset_path = FLAGS.dataset
    
    #dataset = GFDset(dataset_path)
    #print(f"Loaded Dataset from {dataset_path} of size {dataset.num_pairs}")
    
    from gfrl.common.mybase.cloning.dataset import get_datasets
    train_dataset, validation_dataset = get_datasets(dataset_path)
    print(f"Loaded Dataset from {dataset_path}")
    print(f"Train Size: {train_dataset.size}")
    print(f"Validation Size: {validation_dataset.size}")
    print()


    
    #CREATE DIRECTORIES
    import os 
    from gfrl.common import utils

    cwd = os.getcwd()
    exp_root = FLAGS.exp_root
    exp_name = FLAGS.exp_name
    log_path = utils.get_incremental_dirname(exp_root, exp_name)

    #SAVE PARAMETERS
    utils.save_params(log_path, FLAGS)
    
    #print("Logging in ", log_path)
    #print("Log Arguement", FLAGS.log_path)
    os.environ['OPENAI_LOG_FORMAT'] = 'stdout,tensorboard,csv,log'

    configure_logger(log_path=log_path)

    run_raw_gf = FLAGS.run_raw_gf
    print("Run Raw GF: ", run_raw_gf)

    
    if run_raw_gf:
        raise NotImplementedError
        print("Running experiment on Raw GFootball Environment")
        vec_env = SubprocVecEnv([lambda _i=i: \
                                create_single_football_env(_i, level) for i in
                                range(FLAGS.num_envs)], context=None)

    else:
        
        from baselines.common.vec_env.dummy_vec_env import DummyVecEnv

        vec_env = DummyVecEnv([lambda _i=i: \
                        create_single_scenic_environment(_i,FLAGS.level) for i in
                        range(FLAGS.num_envs)])

        if FLAGS.eval_level != "":
            eval_env = DummyVecEnv([lambda _i=i: \
                        create_single_scenic_environment(_i+FLAGS.num_envs, FLAGS.eval_level) for i in
                        range(FLAGS.num_envs)])
        else:
            eval_env = None
            
    
    # Import tensorflow after we create environments. TF is not fork sake, and
    # we could be using TF as part of environment if one of the players is
     # controled by an already trained model.

    import tensorflow.compat.v1 as tf
    #import tensorflow as tf
    
    ncpu = multiprocessing.cpu_count()
    config = tf.ConfigProto(allow_soft_placement=True,
                            intra_op_parallelism_threads=ncpu,
                            inter_op_parallelism_threads=ncpu)
    config.gpu_options.allow_growth = True
    tf.Session(config=config).__enter__()
    
    print(tf.__version__)




    
    from gfrl.common.mybase.cloning import bc
    bc.learn(
        network=FLAGS.policy,
        env=vec_env,
        eval_env = eval_env,
        n_epochs=FLAGS.n_epochs,
        batch_size=FLAGS.batch_size,
        seed=FLAGS.seed,
        nsteps=FLAGS.nsteps,
        nminibatches=FLAGS.nminibatches,
        lr=FLAGS.lr,
        log_interval=1,
        eval_interval=FLAGS.eval_interval,
        eval_timesteps=FLAGS.eval_timesteps,
        save_interval=FLAGS.save_interval,
        dataset = train_dataset,
        validation_dataset = validation_dataset
        )


if __name__ == '__main__':
    app.run(train)