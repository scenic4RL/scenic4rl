"""Simple example of writing experiences to a file using JsonWriter."""

import gym
import numpy as np
import os

from ray.rllib.models.preprocessors import get_preprocessor
from ray.rllib.evaluation.sample_batch_builder import SampleBatchBuilder
from ray.rllib.offline.json_writer import JsonWriter
from tqdm import tqdm

from scenic.simulators.gfootball.rl.gfScenicEnv_v3 import GFScenicEnv_v3
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

if __name__ == "__main__":
    batch_builder = SampleBatchBuilder()  # or MultiAgentSampleBatchBuilder
    writer = JsonWriter(
        os.path.join("remove_offline0")
    )

    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring',
        "representation": 'extracted',
        # "channel_dimensions": (42, 42)
        "dump_full_episodes": True,
        "dump_scores": True,
        "tracesdir": "/home/mark/workplace/gf/scenic4rl/replays",
        "write_video": True,
    }

    # from scenic.simulators.gfootball.rl.gfScenicEnv_v3 import GFScenicEnv_v3

    num_trials = 500
    scenario_file = "/home/mark/workplace/gf/scenic4rl/training/gfrl/_scenarios/demonstration/offense_avoid_pass_shoot.scenic"
    scenario = buildScenario(scenario_file)

    env = GFScenicEnv_v3(initial_scenario=scenario, player_control_mode="allNonGK", gf_env_settings=gf_env_settings,
                         allow_render=False)

    # RLlib uses preprocessors to implement transforms such as one-hot encoding
    # and flattening of tuple and dict observations. For CartPole a no-op
    # preprocessor is used, but this may be relevant for more complex envs.
    prep = get_preprocessor(env.observation_space)(env.observation_space)
    print("The preprocessor is", prep)

    total_reward = 0
    for eps_id in tqdm(range(num_trials)):
        obs = env.reset()
        prev_action = np.zeros_like(env.action_space.sample())
        prev_reward = 0
        done = False
        t = 0
        while not done:
            # action = env.action_space.sample()
            action = env.simulation.get_scenic_designated_player_action()

            new_obs, rew, done, info = env.step(action)
            batch_builder.add_values(
                t=t,
                eps_id=eps_id,
                agent_index=0,
                obs=prep.transform(obs),
                actions=action,
                action_prob=1.0,  # put the true action probability here
                action_logp=0.0,
                rewards=rew,
                prev_actions=prev_action,
                prev_rewards=prev_reward,
                dones=done,
                infos=info,
                new_obs=prep.transform(new_obs),
            )
            obs = new_obs
            prev_action = action
            prev_reward = rew
            t += 1
        writer.write(batch_builder.build_and_reset())
        total_reward += prev_reward[0]

    print(f"Done generating data. Policy score: {total_reward/num_trials}")
