from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os
import datetime
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import EvalCallback


from stable_baselines3.common.vec_env import VecEnvWrapper

#from stable_baselines3.common.evaluation import ResultsWriter
import numpy as np
import time
from collections import deque
import os.path as osp
import json
import csv


class ResultsWriter(object):
    def __init__(self, filename, header='', extra_keys=()):
        print('init resultswriter')
        self.extra_keys = extra_keys
        assert filename is not None
        if not filename.endswith(VecMonitor.EXT):
            if osp.isdir(filename):
                filename = osp.join(filename, VecMonitor.EXT)
            else:
                filename = filename #   + "." + VecMonitor.EXT
        self.f = open(filename, "wt")
        if isinstance(header, dict):
            header = '# {} \n'.format(json.dumps(header))
        self.f.write(header)
        self.logger = csv.DictWriter(self.f, fieldnames=('r', 'l', 't')+tuple(extra_keys))
        self.logger.writeheader()
        self.f.flush()

    def write_row(self, epinfo):
        if self.logger:
            self.logger.writerow(epinfo)
            self.f.flush()

"""SEE https://github.com/hill-a/stable-baselines/issues/470"""
class VecMonitor(VecEnvWrapper):
    def __init__(self, venv, filename=None, keep_buf=0, info_keywords=()):
        VecEnvWrapper.__init__(self, venv)
        self.eprets = None
        self.eplens = None
        self.epcount = 0
        self.tstart = time.time()
        if filename:
            self.results_writer = ResultsWriter(filename, header={'t_start': self.tstart},
                extra_keys=info_keywords)
        else:
            self.results_writer = None
        self.info_keywords = info_keywords
        self.keep_buf = keep_buf
        if self.keep_buf:
            self.epret_buf = deque([], maxlen=keep_buf)
            self.eplen_buf = deque([], maxlen=keep_buf)

    def reset(self):
        obs = self.venv.reset()
        self.eprets = np.zeros(self.num_envs, 'f')
        self.eplens = np.zeros(self.num_envs, 'i')
        return obs

    def step_wait(self):
        obs, rews, dones, infos = self.venv.step_wait()
        self.eprets += rews
        self.eplens += 1

        newinfos = list(infos[:])
        for i in range(len(dones)):
            if dones[i]:
                info = infos[i].copy()
                ret = self.eprets[i]
                eplen = self.eplens[i]
                epinfo = {'r': ret, 'l': eplen, 't': round(time.time() - self.tstart, 6)}
                for k in self.info_keywords:
                    epinfo[k] = info[k]
                info['episode'] = epinfo
                if self.keep_buf:
                    self.epret_buf.append(ret)
                    self.eplen_buf.append(eplen)
                self.epcount += 1
                self.eprets[i] = 0
                self.eplens[i] = 0
                if self.results_writer:
                    self.results_writer.write_row(epinfo)
                newinfos[i] = info
        return obs, rews, dones, newinfos

def train(env, eval_env, ALGO, features_extractor_class, scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, dump_info):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)

    #env = Monitor(env)

    policy_kwargs = dict(
        features_extractor_class=features_extractor_class,
        features_extractor_kwargs=dict(features_dim=256),
    )

    parameters = dict(clip_range=0.08, gamma=0.993, learning_rate=0.0003,
                      batch_size=512, n_epochs=10, ent_coef=0.003, max_grad_norm=0.64,
                      vf_coef=0.5, gae_lambda=0.95,
                      scenario=scenario_name)

    model = ALGO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1, tensorboard_log=logdir,
                 clip_range=parameters["clip_range"], gamma=parameters["gamma"],
                 learning_rate=parameters["learning_rate"],
                 batch_size=parameters["batch_size"], n_epochs=parameters["n_epochs"], ent_coef=parameters["ent_coef"],
                 max_grad_norm=parameters["max_grad_norm"], vf_coef=parameters["vf_coef"],
                 gae_lambda=parameters["gae_lambda"])

    # eval_callback = EvalCallback(self.eval_env, best_model_save_path=save_dir,
    #                             log_path=logdir, eval_freq=eval_freq,
    #                             deterministic=True, render=False)

    eval_callback = EvalCallback(eval_env, eval_freq=eval_freq, deterministic=True, render=False)

    currentDT = datetime.datetime.now()
    fstr = f"HM_{currentDT.hour}_{currentDT.minute}__DM_{currentDT.day}_{currentDT.month}"
    log_file_name = f"{fstr}"
    parameter_out_file_name = logdir + '/' + log_file_name + ".param"

    with open(parameter_out_file_name, "w+") as parout:
        other_info = dict(save_dir=save_dir, total_training_timesteps=total_training_timesteps,
                          eval_freq=eval_freq, parameter_out_file_name=parameter_out_file_name)
        other_info.update(parameters)
        other_info.update(dump_info)
        import pprint
        parout.write(pprint.pformat(other_info))

    model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name)  # callback=eval_callback

    model.save(f"{save_dir}/PPO_impala_cnn_{total_training_timesteps}")

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=n_eval_episodes)

    eval_str = f"\nEval Mean Rewards: {mean_reward:0.4f} Episodes: {n_eval_episodes}\n"
    print(eval_str)

    with open(parameter_out_file_name, "a+") as parout:
        parout.write(eval_str)