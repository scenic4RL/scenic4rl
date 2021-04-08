from scenic.simulators.gfootball import rl_interface
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import pretrain_template
from gfootball_impala_cnn import GfootballImpalaCNN
import gym
from tqdm import tqdm
import numpy as np
import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from stable_baselines3 import PPO, A2C, SAC, TD3
from stable_baselines3.common.evaluation import evaluate_policy

from torch.utils.data.dataset import Dataset, random_split
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

if __name__ == "__main__":

    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    scenario_file = f"{cwd}/pretrain/pass_n_shoot.scenic"
    n_eval_episodes = 10
    total_training_timesteps = 500000
    eval_freq = 10000

    save_dir = f"{cwd}/saved_models_pass_n_shoot_round_2/"
    logdir = f"{cwd}/tboard/pretrain_pass_n_shoot/"
    tracedir = f"{cwd}/game_trace"
    rewards = "scoring"#'scoring,checkpoints'
    
    print("model, tf logs, game trace are saved in: ", save_dir, logdir, tracedir)

    parameter_list = [ 
                        dict(learning_rate=0.0003,batch_size=1024, n_epochs=10, n_steps = 4096, pretraining=False),
                        dict(learning_rate=0.0003,batch_size=1024, n_epochs=10, n_steps = 4096, pretraining=True),
                        dict(learning_rate=0.0003,batch_size=1024, n_epochs=10, n_steps = 8192, pretraining=False),
                        dict(learning_rate=0.0003,batch_size=1024, n_epochs=10, n_steps = 8192, pretraining=True),
                    ]


    for sn in range(len(parameter_list)):
        parameters = parameter_list[sn]
        pretraining = parameters["pretraining"]

        
        gf_env_settings = {
            "stacked": True,
            "rewards": "scoring",
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False,
            "action_set": "default"
        }
        target_scenario_name = f"{cwd}/pretrain/pass_n_shoot.scenic"

        from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
        scenario = buildScenario(target_scenario_name)

        env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False)
        env = Monitor(env)
        
        loaded = PPO.load(f"cnn_adam_pass_n_shoot_20000_50")
        
        model = PPO("CnnPolicy", env, verbose=1, tensorboard_log=logdir, learning_rate=parameters["learning_rate"], 
                                batch_size=parameters["batch_size"], n_epochs=parameters["n_epochs"],
                                n_steps=parameters["n_steps"])

        if pretraining:
            model.policy = loaded.policy 
            print("loaded weights from pretrained agent")
        else:
            print("No Pretraining. Starting with Random weight")

        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(logdir, exist_ok=True)

        eval_callback = MyEvalCallback(model.get_env(), eval_freq=eval_freq, deterministic=True, render=False)

        currentDT = datetime.datetime.now()
        fstr = f"HM_{currentDT.hour}_{currentDT.minute}__DM_{currentDT.day}_{currentDT.month}"
        log_file_name = f"{fstr}"

        print("tboard name", log_file_name)

        model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name,
            callback=eval_callback) 

        model_name = "PPO_nature_cnn_pass_n_shoot"
        if pretraining: model_name += "_warm_start"
        model_name+=f"{sn}"
        model.save(f"{save_dir}/{model_name}_{total_training_timesteps}")
        print("-------------")