"""A simple example of setting up a multi-agent version of GFootball with rllib.
"""

import argparse
import ray
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.models import ModelCatalog

from gfrl.common.nature_cnn import NatureCNN
from gfrl.common.rllibGFootballEnv import RllibGFootball

# scenario mapping
scenario_name_to_file = {
    "defender_hesitantdribble":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/defender_vs_opponent_with_hesitant_dribble.scenic",
    "defender_zigzagdribble":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/defender_vs_opponent_with_zigzag_dribble.scenic",
    "2v2":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/2vs2.scenic",
    "2v2_counterattack":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/2vs2_counterattack.scenic",
    "2v2_highpassforward":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/2vs2_with_scenic_high_pass_forward.scenic",
    "3v2_counterattack":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/3vs2_counterattack.scenic",
    "3v2_crossfromside":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/3vs3_cross_from_side.scenic",
    "3v2_sidebuildup":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/defense/3vs3_side_buildup_play.scenic",

    "grf_passshoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/grf/pass_n_shoot.scenic",
    "grf_runtoscore":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/grf/rts.scenic",
    "grf_runpassshoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/grf/run_pass_shoot.scenic",
    "offense_11gk":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/offense/11_vs_GK.scenic",
    "offense_avoidpassshoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/offense/avoid_pass_shoot.scenic",
    "offense_easycross":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/offense/easy_crossing.scenic",
    "offense_hardcross":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/offense/hard_crossing.scenic",

}


# running exps
parser = argparse.ArgumentParser()

parser.add_argument('--scenario', type=str)
parser.add_argument('--mode', type=str, default="allNonGK")
parser.add_argument('--num-steps', type=int, default=5000000)
parser.add_argument('--id', type=int, default=0)

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
        "evaluation_interval": 50,
        "evaluation_duration": 100,
        "evaluation_duration_unit": "episodes",

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

    tune.run(
        'PPO',
        name=f"aaai{args.id}_{args.scenario}_{args.mode}",
        stop={'timesteps_total': args.num_steps},
        checkpoint_freq=50,
        config=rl_trainer_config,
    )
