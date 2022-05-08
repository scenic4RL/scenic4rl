"""A simple example of setting up a multi-agent version of GFootball with rllib.
"""
import os
import argparse
import sys
import ray
import pickle
from ray import tune
from ray.rllib.agents.registry import get_trainer_class
from ray.rllib.agents.ppo import PPOTrainer
from gfrl.common.rllibGFootballEnv import RllibGFootball
from ray.tune.registry import register_env
from ray.rllib.models import ModelCatalog

from gfrl.common.nature_cnn import NatureCNN

# scenario mapping
scenario_name_to_file = {
    "offense_avoid_pass_shoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/offense/avoid_pass_shoot.scenic",
    "offense_11_vs_gk":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/offense/11_vs_GK.scenic",
    "offense_counterattack_easy":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/grf/counterattack_easy.scenic"
    "grf_passshoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/grf/pass_n_shoot.scenic"
}

class LoadablePPOTrainer(PPOTrainer):
    def __init__(self, config, **kwargs):
        bc_store_path = config["bc_store_path"]
        del config["bc_store_path"]
        super(LoadablePPOTrainer, self).__init__(config, **kwargs)
        # load weights
        bc_weights = pickle.load(open(bc_store_path, "rb"))
        self.set_weights(bc_weights)
        print(f"Loaded weights from {bc_store_path}")


# running exps
parser = argparse.ArgumentParser()

parser.add_argument('--scenario', type=str)
parser.add_argument('--mode', type=str)
parser.add_argument('--demonstration-file', type=str)
parser.add_argument('--resumebc', action='store_true')
parser.add_argument('--id', type=str, default="0")
parser.add_argument('--num-bc-steps', type=int, default=2000000)
parser.add_argument('--num-ppo-steps', type=int, default=5000000)
parser.add_argument('--bc-weights-dir', type=str, default="/home/qcwu/gf/scenic4rl/training/gfrl/_bc_weights")

if __name__ == '__main__':
    args = parser.parse_args()
    assert args.scenario in scenario_name_to_file, "invalid scenario name"
    scenario_file = scenario_name_to_file[args.scenario]

    ray.init(num_gpus=1)
    # Simple environment with input multi agent control mode
    register_env('gfootball', lambda config: RllibGFootball(scenario_file, args.mode, config))
    single_env = RllibGFootball(scenario_file, args.mode)
    obs_space = single_env.observation_space
    act_space = single_env.action_space
    num_policies = single_env.num_agents


    def gen_policy(_):
        return (None, obs_space, act_space, {})


    # Setup PPO with an ensemble of `num_policies` different policies
    policies = {
        'policy_{}'.format(i): gen_policy(i) for i in range(num_policies)
    }
    policy_ids = list(policies.keys())

    # set up model
    ModelCatalog.register_custom_model("nature_cnn", NatureCNN)

    # set up config
    rl_trainer_config = {
        'env': 'gfootball',
        "framework": "torch",
        # === Input settings ===
        "input": args.demonstration_file,
        # "input_config": {},

        # === Postprocessing/accum., discounted return calculation ===
        "use_gae": True,
        "input_evaluation": [],
        "postprocess_inputs": False,

        # === Training ===
        # Scaling of advantages in exponential terms.
        # When beta is 0.0, MARWIL is reduced to behavior cloning
        # (imitation learning); see bc.py algorithm in this same directory.
        "beta": 0.0,
        # Balancing value estimation loss and policy optimization loss.
        "vf_coeff": 1.0,
        # If specified, clip the global norm of gradients by this amount.
        "grad_clip": None,
        # Learning rate for Adam optimizer.
        "lr": 0.00008,
        # The squared moving avg. advantage norm (c^2) update rate
        # (1e-8 in the paper).
        "moving_average_sqd_adv_norm_update_rate": 1e-8,
        # Starting value for the squared moving avg. advantage norm (c^2).
        "moving_average_sqd_adv_norm_start": 100.0,
        # Number of (independent) timesteps pushed through the loss
        # each SGD round.
        "train_batch_size": 2000,
        # Size of the replay buffer in (single and independent) timesteps.
        # The buffer gets filled by reading from the input files line-by-line
        # and adding all timesteps on one line at once. We then sample
        # uniformly from the buffer (`train_batch_size` samples) for
        # each training step.
        "replay_buffer_size": 10000,
        # Number of steps to read before learning starts.
        "learning_starts": 0,

        # === Parallelism ===
        # Which observation filter to apply to the observation.
        "observation_filter": "NoFilter",
        'num_gpus': 1,
        'num_workers': 14,
        'num_envs_per_worker': 1,
        'log_level': 'INFO',
        "evaluation_num_workers": 1,
        "evaluation_interval": 100,
        "evaluation_config": {"input": "sampler"},


        # All model-related settings go into this sub-dict.
        "model": {
            "custom_model": "nature_cnn",
            "custom_model_config": {},
        },
        'multiagent': {
            'policies': policies,
            'policy_mapping_fn':
                lambda agent_id, episode, worker, **kwargs: policy_ids[int(agent_id[6:])],
        }
    }

    bc_exp_name = f"bc_{args.scenario}_{args.mode}_0"

    if not args.resumebc:
        bc_results = tune.run(
            'BC',
            name=bc_exp_name,
            stop={'timesteps_total': args.num_bc_steps},
            checkpoint_freq=50,
            config=rl_trainer_config,
            checkpoint_at_end=True,
            resume=args.resumebc
        )

        print("Training completed. Restoring new Trainer for action inference.")
        # Get the last checkpoint from the above training run.
        checkpoint = bc_results.get_last_checkpoint()
        # Create new Trainer and restore its state from the last checkpoint.
        trainer = get_trainer_class('BC')(config=rl_trainer_config)
        trainer.restore(checkpoint)
        bcweights = trainer.get_weights()

        os.makedirs(args.bc_weights_dir, exist_ok = True)
        bc_store_path = os.path.join(args.bc_weights_dir, bc_exp_name+".pkl")
        pickle.dump(bcweights, open(bc_store_path, "wb"))
        print(f"Stored bcweights to {bc_store_path}")
        print("Run with resumebc option to pretrain.")
        sys.exit()

    # --- PPO Training ---
    bc_store_path = os.path.join(args.bc_weights_dir, bc_exp_name+".pkl")


    # PPO config
    ppo_trainer_config = {
        'env': 'gfootball',
        "framework": "torch",
        # Discount factor of the MDP.
        "gamma": 0.993,
        # Should use a critic as a baseline (otherwise don't use value baseline;
        # required for using GAE).
        "use_critic": True,
        # If true, use the Generalized Advantage Estimator (GAE)
        # with a value function, see https://arxiv.org/pdf/1506.02438.pdf.
        "use_gae": True,
        # The GAE (lambda) parameter.
        "lambda": 0.95,
        # Initial coefficient for KL divergence.
        "kl_coeff": 0.2,
        # Size of batches collected from each worker.
        "rollout_fragment_length": 200,
        # Number of timesteps collected for each SGD round. This defines the size
        # of each SGD epoch.
        "train_batch_size": 4000,
        # Total SGD batch size across all devices for SGD. This defines the
        # minibatch size within each epoch.
        "sgd_minibatch_size": 1000,
        # Whether to shuffle sequences in the batch when training (recommended).
        "shuffle_sequences": True,
        # Number of SGD iterations in each outer loop (i.e., number of epochs to
        # execute per train batch).
        "num_sgd_iter": 10,
        # Stepsize of SGD. 2.5e-4
        "lr": 0.00008,
        # Learning rate schedule.
        "lr_schedule": None,
        # Coefficient of the value function loss. IMPORTANT: you must tune this if
        # you set vf_share_layers=True inside your model's config.
        "vf_loss_coeff": 0.5,
        # Coefficient of the entropy regularizer.
        "entropy_coeff": 0.01,
        # Decay schedule for the entropy regularizer.
        "entropy_coeff_schedule": None,
        # PPO clip parameter.
        "clip_param": 0.27,
        # Clip param for the value function. Note that this is sensitive to the
        # scale of the rewards. If your expected V is large, increase this.
        "vf_clip_param": 10.0,
        # If specified, clip the global norm of gradients by this amount.
        "grad_clip": 0.5,
        # Target value for KL divergence.
        "kl_target": 0.01,
        # Whether to rollout "complete_episodes" or "truncate_episodes".
        "batch_mode": "truncate_episodes",
        # Which observation filter to apply to the observation.
        "observation_filter": "NoFilter",
        'num_gpus': 1,
        'num_workers': 15,
        'num_envs_per_worker': 1,
        'log_level': 'INFO',
        # All model-related settings go into this sub-dict.
        "model": {
            "custom_model": "nature_cnn",
            "custom_model_config": {},
        },
        'multiagent': {
            'policies': policies,
            'policy_mapping_fn':
                lambda agent_id, episode, worker, **kwargs: policy_ids[int(agent_id[6:])],
        }
    }

    # bc_store_path = "/home/qcwu/gf/scenic4rl/training/gfrl/_bc_weights/bc_offense_avoid_pass_shoot_allNonGK_0.pkl"
    ppo_trainer_config["bc_store_path"] = bc_store_path

    tune.run(
        LoadablePPOTrainer,
        name=f"bc_pretrain_{args.scenario}_{args.mode}_{args.id}",
        stop={'timesteps_total': args.num_ppo_steps},
        checkpoint_freq=50,
        config=ppo_trainer_config,
    )


    ray.shutdown()
