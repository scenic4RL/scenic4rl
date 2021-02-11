import gym
import pfrl
from pfrl import experiments, explorers, q_functions, replay_buffers, utils
import gym
import torch

# https://github.com/pfnet/pfrl

def make_env(env, test):
    #env_seed = 2 ** 32 - 1 - args.seed if test else args.seed
    #env.seed(env_seed)
    # Cast observations to float32 because our model uses float32
    env = pfrl.wrappers.CastObservationToFloat32(env)
    #if args.monitor:
    #    env = pfrl.wrappers.Monitor(env, args.outdir)
    #if not test:
        # Scale rewards (and thus returns) to a reasonable range so that
        # training is easier
        #env = pfrl.wrappers.ScaleReward(env, args.reward_scale_factor)
    #if (args.render_eval and test) or (args.render_train and not test):
    #    env = pfrl.wrappers.Render(env)
    return env

def pfrl_training(env):

    #Action Space: Discrete
    #Observation Space: Box(0, 255, (72, 96, 16), uint8)
    x=1
    bs_size = env.observation_space.low.size
    action_space = env.action_space

