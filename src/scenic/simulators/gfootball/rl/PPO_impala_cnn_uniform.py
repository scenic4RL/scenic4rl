import socket
import warnings
from typing import Union

import gym
from scenic.simulators.gfootball.rl.UnifromTeacherEnvironment import UnifromTeacherEnvironment
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os
import datetime
from stable_baselines3.common.callbacks import BaseCallback, EventCallback
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.preprocessing import is_image_space
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.vec_env import VecEnv
from torch import nn
import torch as th
from typing import Union, List, Dict, Any, Optional
from stable_baselines3.common.vec_env import VecEnv, sync_envs_normalization, DummyVecEnv
import numpy as np
class GfootballImpalaCNN(BaseFeaturesExtractor):
    """
    gfootball_impala_cnn is architecture used in the paper
    (https://arxiv.org/pdf/1907.11180.pdf).
    It is illustrated in the appendix. It is similar to Large architecture
    from IMPALA paper; we use 4 big blocks instead of 3 though.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        super(GfootballImpalaCNN, self).__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        assert is_image_space(observation_space), (
            "You should use CNN only with images"
        )
        assert features_dim==256, "To replicate the same network"
        n_input_channels = observation_space.shape[0]

        self.conv_layers_config = [(16, 2), (32, 2), (32, 2), (32, 2)]
        self.pool = nn.MaxPool2d(kernel_size=3, stride=2)


        self.conv_blocks = [
            nn.Conv2d(in_channels=n_input_channels, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1)
        ]

        #https://www.tensorflow.org/api_docs/python/tf/nn/pool  -> If padding = "SAME": output_spatial_shape[i] = ceil(input_spatial_shape[i] / strides[i])
        self.pools = [nn.MaxPool2d(kernel_size=3, stride=2, padding=1) for _ in range(4)]

        self.resblocks_1 = [
            self.create_basic_res_block(16, 16),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32)
        ]
        self.resblocks_2 = [
            self.create_basic_res_block(16, 16),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32)
        ]

        self.relu = nn.ReLU()
        self.flatten = nn.Flatten()


        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.feat_extract(
                th.as_tensor(observation_space.sample()[None]).float()
            )
            n_flatten = n_flatten.shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU()) #n_flatten=960


    def create_basic_res_block(self, in_channel, out_channel):
        return nn.Sequential(
            nn.ReLU(),
            nn.Conv2d(in_channels=in_channel, out_channels=out_channel, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=out_channel, out_channels=out_channel, kernel_size=3, stride=1, padding=1),
        )

    def feat_extract(self, observations: th.Tensor) -> th.Tensor:
        observations = th.FloatTensor(observations)
        observations /= 255

        conv_out = observations
        for i in range(4):
            conv_out = self.conv_blocks[i](conv_out)
            conv_out = self.pools[i](conv_out)

            block_input = conv_out
            conv_out = self.resblocks_1[i](conv_out)
            conv_out += block_input

            block_input = conv_out
            conv_out = self.resblocks_2[i](conv_out)
            conv_out += block_input

        conv_out = self.relu(conv_out)
        conv_out = self.flatten(conv_out)
        return conv_out

    def forward(self, observations: th.Tensor) -> th.Tensor:
        conv_out = self.feat_extract(observations)
        conv_out = self.linear(conv_out)

        return conv_out

class MyEvalCallback(EventCallback):
    def __init__(
        self,
        eval_env: Union[gym.Env, VecEnv],
        callback_on_new_best: Optional[BaseCallback] = None,
        n_eval_episodes: int = 5,
        eval_freq: int = 10000,
        log_path: str = None,
        best_model_save_path: str = None,
        deterministic: bool = True,
        render: bool = False,
        verbose: int = 1,
    ):
        super(MyEvalCallback, self).__init__(callback_on_new_best, verbose=verbose)
        self.n_eval_episodes = n_eval_episodes
        self.eval_freq = eval_freq
        self.best_mean_reward = -np.inf
        self.last_mean_reward = -np.inf
        self.deterministic = deterministic
        self.render = render

        # Convert to VecEnv for consistency
        if not isinstance(eval_env, VecEnv):
            eval_env = DummyVecEnv([lambda: eval_env])

        if isinstance(eval_env, VecEnv):
            assert eval_env.num_envs == 1, "You must pass only one environment for evaluation"

        self.eval_env = eval_env
        self.best_model_save_path = best_model_save_path
        # Logs will be written in ``evaluations.npz``
        if log_path is not None:
            log_path = os.path.join(log_path, "evaluations")
        self.log_path = log_path
        self.evaluations_results = []
        self.evaluations_timesteps = []
        self.evaluations_length = []

    def _init_callback(self) -> None:
        # Does not work in some corner cases, where the wrapper is not the same
        if not isinstance(self.training_env, type(self.eval_env)):
            warnings.warn("Training and eval env are not of the same type" f"{self.training_env} != {self.eval_env}")

        # Create folders if needed
        if self.best_model_save_path is not None:
            os.makedirs(self.best_model_save_path, exist_ok=True)
        if self.log_path is not None:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _on_step(self) -> bool:

        if self.eval_freq > 0 and self.n_calls % self.eval_freq == 0:
            # Sync training and eval env if there is VecNormalize
            sync_envs_normalization(self.training_env, self.eval_env)

            venv = self.eval_env
            ev_env = venv.venv.envs[0]
            ev_env.set_evalautaion_status(True)

            episode_rewards, episode_lengths = evaluate_policy(
                self.model,
                self.eval_env,
                n_eval_episodes=self.n_eval_episodes,
                render=self.render,
                deterministic=self.deterministic,
                return_episode_rewards=True,
            )

            if self.log_path is not None:
                self.evaluations_timesteps.append(self.num_timesteps)
                self.evaluations_results.append(episode_rewards)
                self.evaluations_length.append(episode_lengths)
                np.savez(
                    self.log_path,
                    timesteps=self.evaluations_timesteps,
                    results=self.evaluations_results,
                    ep_lengths=self.evaluations_length,
                )

            mean_reward, std_reward = np.mean(episode_rewards), np.std(episode_rewards)
            mean_ep_length, std_ep_length = np.mean(episode_lengths), np.std(episode_lengths)
            self.last_mean_reward = mean_reward

            if self.verbose > 0:
                print(f"Eval num_timesteps={self.num_timesteps}, " f"episode_reward={mean_reward:.2f} +/- {std_reward:.2f}")
                print(f"Episode length: {mean_ep_length:.2f} +/- {std_ep_length:.2f}")
            # Add to current Logger
            self.logger.record("eval/mean_reward", float(mean_reward))
            self.logger.record("eval/mean_ep_length", mean_ep_length)

            if mean_reward > self.best_mean_reward:
                if self.verbose > 0:
                    print("New best mean reward!")
                if self.best_model_save_path is not None:
                    self.model.save(os.path.join(self.best_model_save_path, "best_model"))
                self.best_mean_reward = mean_reward
                # Trigger callback if needed
                if self.callback is not None:
                    return self._on_event()

            ev_env.set_evalautaion_status(False)

        return True

    def update_child_locals(self, locals_: Dict[str, Any]) -> None:
        """
        Update the references to the local variables.

        :param locals_: the local variables during rollout collection
        """
        if self.callback:
            self.callback.update_locals(locals_)

class PPO_GF_Impala_Uniform_Curriculum:

    def __init__(self, target, sub_tasks):
        self.target = target
        self.sub_tasks = sub_tasks

        self.rl_env = UnifromTeacherEnvironment(target_task=target, sub_tasks=sub_tasks)

    def train(self):
        ALGO = PPO
        n_eval_episodes = 10
        total_training_timesteps = 1000000
        eval_freq = 10000

        save_dir = "./saved_models"
        logdir = "./tboard"

        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(logdir, exist_ok=True)

        env = self.rl_env
        env = Monitor(env)

        policy_kwargs = dict(
            features_extractor_class=GfootballImpalaCNN,
            features_extractor_kwargs=dict(features_dim=256),
        )
        model = ALGO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1, tensorboard_log=logdir,
                     clip_range=0.08, gamma=0.993, learning_rate = 0.0003, batch_size=512,
                     n_epochs=4, ent_coef=0.003, max_grad_norm=0.64,
                     vf_coef=0.5, gae_lambda = 0.95)

        #venv = model.get_env()
        #ev_env = venv.venv.envs[0]
        #ev_env.set_evalautaion_status(True)

        eval_callback = MyEvalCallback(model.get_env(), eval_freq=eval_freq, deterministic=True, render=False)
        #ev_env.set_evalautaion_status(False)

        currentDT = datetime.datetime.now()
        fstr = f"HM_{currentDT.hour}_{currentDT.minute}__DM_{currentDT.day}_{currentDT.month}"
        model.learn(total_timesteps=total_training_timesteps, tb_log_name=f"{socket.gethostname()}_{fstr}", callback=eval_callback) #callback=eval_callback

        model.save(f"{save_dir}/PPO_impala_cnn_{total_training_timesteps}")

        mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=n_eval_episodes)
        print(f"Eval Mean Rewards: {mean_reward:0.4f} Episodes: {n_eval_episodes}")




if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    # scenario_file = f"{cwd}/academy/academy_run_pass_and_shoot_with_keeper.scenic"

    # n_task = 3

    target_task = f"{cwd}/exp_0_1/empty_goal.scenic"
    subtasks = [
        f"{cwd}/exp_0_1/empty_goal_0.scenic",
        f"{cwd}/exp_0_1/empty_goal_1.scenic",
        f"{cwd}/exp_0_1/empty_goal_2.scenic",
        f"{cwd}/exp_0_1/empty_goal_3.scenic",
        f"{cwd}/exp_0_1/empty_goal_4.scenic",
        f"{cwd}/exp_0_1/empty_goal_5.scenic",
        f"{cwd}/exp_0_1/empty_goal_6.scenic",
        f"{cwd}/exp_0_1/empty_goal_7.scenic",
    ]
    # scenario_files = [target_task] + subtasks

    # for i in range(n_task):
    #    name = f"{cwd}/academy/academy_run_pass_and_shoot_with_keeper_task_{i}.scenic"
    #    scenario_files.append(name)

    # scenario = buildScenario(scenario_file)
    PPO_GF_Impala_Uniform_Curriculum(target_task, subtasks).train()


"""
HT 0:  on exp_0_0/academy_run_pass_and_shoot_with_keeper.scenic
ALGO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1, tensorboard_log=logdir,
                     clip_range=0.08, gamma=0.993, learning_rate = 0.000343, batch_size=512,
                     n_epochs=2, ent_coef=0.003, max_grad_norm=0.64,
                     vf_coef=0.5, gae_lambda = 0.95)
"""