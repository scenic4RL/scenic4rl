from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os
import datetime
import gym
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.callbacks import BaseCallback, EventCallback
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
import warnings
from typing import Union
from stable_baselines3.common import results_plotter
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results

from stable_baselines3.common.callbacks import BaseCallback

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

            if hasattr(ev_env, "set_evalautaion_status"):
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

            if hasattr(ev_env, "set_evalautaion_status"):
                ev_env.set_evalautaion_status(False)

        return True

    def update_child_locals(self, locals_: Dict[str, Any]) -> None:
        """
        Update the references to the local variables.

        :param locals_: the local variables during rollout collection
        """
        if self.callback:
            self.callback.update_locals(locals_)

class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq: (int)
    :param log_dir: (str) Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: (int)
    """
    def __init__(self, check_freq: int, log_dir: str, verbose=1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, 'best_model')
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

          # Retrieve training reward
          x, y = ts2xy(load_results(self.log_dir), 'timesteps')
          if len(x) > 0:
              # Mean training reward over the last 100 episodes
              mean_reward = np.mean(y[-100:])
              if self.verbose > 0:
                print("Num timesteps: {}".format(self.num_timesteps))
                print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(self.best_mean_reward, mean_reward))

              # New best model, you could save the agent here
              if mean_reward > self.best_mean_reward:
                  self.best_mean_reward = mean_reward
                  # Example for saving best model
                  if self.verbose > 0:
                    print("Saving new best model to {}".format(self.save_path))
                  self.model.save(self.save_path)

        return True
def train(env, ALGO, features_extractor_class, scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, dump_info, override_params={}, rewards=""):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)

    
    
    currentDT = datetime.datetime.now()
    fstr = f"HM_{currentDT.hour}_{currentDT.minute}__DM_{currentDT.day}_{currentDT.month}"
    log_file_name = f"{fstr}"
    parameter_out_file_name = logdir + '/' + log_file_name + ".param"

    monitor_dir = logdir + '/monitor_' +  log_file_name
    os.makedirs(monitor_dir, exist_ok=True)
    env = Monitor(env, filename=monitor_dir)

    policy_kwargs = dict(
        features_extractor_class=features_extractor_class,
        features_extractor_kwargs=dict(features_dim=256),
    )

    if rewards=='scoring,checkpoints':
        print("Using scoring,checkpoints Parameters")
        parameters = dict(clip_range=0.08, gamma=0.993, learning_rate=0.0003,
                          batch_size=512, n_epochs=10, ent_coef=0.003, max_grad_norm=0.64,
                          vf_coef=0.5, gae_lambda=0.95, n_steps = 2048,
                          scenario=scenario_name)
    else:
        print("Using scoring Parameters")
        parameters = dict(clip_range=0.115, gamma=0.997, learning_rate=0.00011879,
                          batch_size=512, n_epochs=10, ent_coef=0.00155, max_grad_norm=0.76,
                          vf_coef=0.5, gae_lambda=0.95, n_steps = 2048,
                          scenario=scenario_name)

    parameters.update(override_params)


    model = ALGO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1, tensorboard_log=logdir,
                 clip_range=parameters["clip_range"], gamma=parameters["gamma"],
                 learning_rate=parameters["learning_rate"],
                 batch_size=parameters["batch_size"], n_epochs=parameters["n_epochs"], ent_coef=parameters["ent_coef"],
                 max_grad_norm=parameters["max_grad_norm"], vf_coef=parameters["vf_coef"],
                 gae_lambda=parameters["gae_lambda"])

    # eval_callback = EvalCallback(self.eval_env, best_model_save_path=save_dir,
    #                             log_path=logdir, eval_freq=eval_freq,
    #                             deterministic=True, render=False)

    eval_callback = MyEvalCallback(model.get_env(), eval_freq=eval_freq, deterministic=True, render=False)

    save_best_trainied_model = SaveOnBestTrainingRewardCallback(check_freq=eval_freq, log_dir = monitor_dir)

    

    with open(parameter_out_file_name, "w+") as parout:
        other_info = dict(save_dir=save_dir, total_training_timesteps=total_training_timesteps,
                          eval_freq=eval_freq, parameter_out_file_name=parameter_out_file_name)
        other_info.update(parameters)
        other_info.update(dump_info)
        import pprint
        parout.write(pprint.pformat(other_info))

    model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name,
                callback=[eval_callback, save_best_trainied_model])  # callback=eval_callback

    model.save(f"{save_dir}/PPO_{fstr}_{total_training_timesteps}")

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=n_eval_episodes)

    eval_str = f"\nEval Mean Rewards: {mean_reward:0.4f} Episodes: {n_eval_episodes}\n"
    print(eval_str)

    with open(parameter_out_file_name, "a+") as parout:
        parout.write(eval_str)



