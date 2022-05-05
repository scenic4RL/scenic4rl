"""Simple example of writing experiences to a file using JsonWriter."""
from typing import Optional

import argparse
import numpy as np
import os

from ray.rllib.agents import DefaultCallbacks
from ray.rllib.evaluation.episode import Episode
from ray.rllib.models.preprocessors import get_preprocessor
from ray.rllib.evaluation.sample_batch_builder import SampleBatchBuilder, MultiAgentSampleBatchBuilder
from ray.rllib.offline.json_writer import JsonWriter
from tqdm import tqdm

from gfrl.common.rllibGFootballEnv import RllibGFootball


class ScenicSampleBatchBuilder(MultiAgentSampleBatchBuilder):
    def postprocess_batch_so_far(self,
                                 episode: Optional[Episode] = None) -> None:
        """Apply policy postprocessors to any unprocessed rows.

        This pushes the postprocessed per-agent batches onto the per-policy
        builders, clearing per-agent state.

        Args:
            episode (Optional[Episode]): The Episode object that
                holds this MultiAgentBatchBuilder object.
        """

        # Materialize the batches so far.
        pre_batches = {}
        for agent_id, builder in self.agent_builders.items():
            pre_batches[agent_id] = (
                self.policy_map[self.agent_to_policy[agent_id]],
                builder.build_and_reset())

        # Apply postprocessor.
        post_batches = {}
        if self.clip_rewards is True:
            for _, (_, pre_batch) in pre_batches.items():
                pre_batch["rewards"] = np.sign(pre_batch["rewards"])
        elif self.clip_rewards:
            for _, (_, pre_batch) in pre_batches.items():
                pre_batch["rewards"] = np.clip(
                    pre_batch["rewards"],
                    a_min=-self.clip_rewards,
                    a_max=self.clip_rewards)
        for agent_id, (_, pre_batch) in pre_batches.items():
            other_batches = pre_batches.copy()
            del other_batches[agent_id]
            policy = self.policy_map[self.agent_to_policy[agent_id]]
            if any(pre_batch["dones"][:-1]) or len(set(
                    pre_batch["eps_id"])) > 1:
                raise ValueError(
                    "Batches sent to postprocessing must only contain steps "
                    "from a single trajectory.", pre_batch)
            # Call the Policy's Exploration's postprocess method.
            post_batches[agent_id] = pre_batch
            # if getattr(policy, "exploration", None) is not None:
            #     policy.exploration.postprocess_trajectory(
            #         policy, post_batches[agent_id], policy.get_session())
            # post_batches[agent_id] = policy.postprocess_trajectory(
            #     post_batches[agent_id], other_batches, episode)

        # Append into policy batches and reset
        for agent_id, post_batch in sorted(post_batches.items()):
            self.policy_builders[self.agent_to_policy[agent_id]].add_batch(
                post_batch)

        self.agent_builders.clear()
        self.agent_to_policy.clear()

# scenario mapping
scenario_name_to_file = {
    "offense_avoid_pass_shoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/demonstration_multirl/offense_avoid_pass_shoot.scenic",
    "offense_11_vs_gk":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/demonstration_multirl/offense_11_vs_GK.scenic",
    "offense_counterattack_easy":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/demonstration_multirl/counterattack_easy.scenic",
    "grf_passshoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/demonstration_multirl/rl_pass_and_shoot_with_keeper.scenic",
}

# running exps
parser = argparse.ArgumentParser()

parser.add_argument('--scenario', type=str, default="offense_11_vs_gk")
parser.add_argument('--mode', type=str, default="3")
parser.add_argument('--num-samples', type=int, default=8000)


if __name__ == "__main__":
    args = parser.parse_args()
    assert args.scenario in scenario_name_to_file, "invalid scenario name"
    scenario_file = scenario_name_to_file[args.scenario]
    control_mode = args.mode

    out_directory_path = f"offline_ni_{args.scenario}"
    num_trials = args.num_samples
    

    env = RllibGFootball(scenario_file, control_mode)
    obs_space = env.observation_space
    act_space = env.action_space
    num_policies = env.num_agents
    num_agents = num_policies  # we use 1:1 agent policy mapping

    def gen_policy(_):
        return (None, obs_space, act_space, {})

    # Setup PPO with an ensemble of `num_policies` different policies
    policies = {
        'policy_{}'.format(i): gen_policy(i) for i in range(num_policies)
    }

    # Generate Data
    batch_builder = ScenicSampleBatchBuilder(policies, False, DefaultCallbacks())  # or MultiAgentSampleBatchBuilder
    writer = JsonWriter(out_directory_path)

    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring',
        "representation": 'extracted',
        "dump_full_episodes": False,
        "dump_scores": False,
        "tracesdir": "/home/qcwu/gf/scenic4rl/replays",
        "write_video": False,
    }
    # RLlib uses preprocessors to implement transforms such as one-hot encoding
    # and flattening of tuple and dict observations. For CartPole a no-op
    # preprocessor is used, but this may be relevant for more complex envs.
    prep = get_preprocessor(env.observation_space)(env.observation_space)
    print("The preprocessor is", prep)

    # generating data
    pbar = tqdm(total=num_trials)
    eps_id = 0
    total_attempts = 0
    total_reward = 0
    while eps_id < num_trials:
        total_attempts += 1
        obs_dict = env.reset()
        prev_action_dict = {f"agent_{i}": np.zeros_like(env.action_space.sample()) for i in range(num_agents)}
        prev_reward_dict = {f"agent_{i}": 0 for i in range(num_agents)}
        done = False
        t = 0
        while not done:
            # action = env.action_space.sample()
            action = env.env.simulation.get_scenic_designated_player_action()
            action_dict = {f"agent_{i}": action[i] for i in range(num_agents)}

            new_obs_dict, rew_dict, done_dict, info_dict = env.step(action_dict)
            done = done_dict["__all__"]

            for i in range(num_agents):
                agent_id = f"agent_{i}"
                policy_id = f"policy_{i}"
                batch_builder.add_values(
                    agent_id,
                    policy_id,
                    t=t,
                    eps_id=eps_id,
                    agent_index=i,
                    obs=prep.transform(obs_dict[agent_id]),
                    actions=action_dict[agent_id],
                    action_prob=1.0,  # put the true action probability here
                    action_logp=0.0,
                    rewards=rew_dict[agent_id],
                    prev_actions=prev_action_dict[agent_id],
                    prev_rewards=prev_reward_dict[agent_id],
                    dones=done,
                    infos=None, # info is skipped to reduce file size
                    new_obs=prep.transform(new_obs_dict[agent_id]),
                )
            obs_dict = new_obs_dict
            prev_action_dict = action_dict
            prev_reward_dict = rew_dict
            t += 1
        batch_builder.count = t

        # we only record if this run scores 
        candidate_batch = batch_builder.build_and_reset()
        if prev_reward_dict["agent_0"] == 1:
            writer.write(candidate_batch)
            eps_id += 1
            total_reward += prev_reward_dict["agent_0"]
            pbar.update(1)
        
    pbar.close()
    print(f"Done generating data. Dataset score: {total_reward/num_trials}. Avg Score: {total_reward/total_attempts}.")
