from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os
import datetime
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import EvalCallback


def train(env, ALGO, features_extractor_class, scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, dump_info):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)

    env = Monitor(env)

    policy_kwargs = dict(
        features_extractor_class=features_extractor_class,
        features_extractor_kwargs=dict(features_dim=256),
    )

    parameters = dict(clip_range=0.08, gamma=0.993, learning_rate=0.0003,
                      batch_size=512, n_epochs=10, ent_coef=0.003, max_grad_norm=0.64,
                      vf_coef=0.5, gae_lambda=0.95, n_steps = 2048,
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

    eval_callback = EvalCallback(model.get_env(), eval_freq=eval_freq, deterministic=True, render=False)

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

    model.learn(total_timesteps=total_training_timesteps, tb_log_name=log_file_name,
                callback=eval_callback)  # callback=eval_callback

    model.save(f"{save_dir}/PPO_impala_cnn_{total_training_timesteps}")

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=n_eval_episodes)

    eval_str = f"\nEval Mean Rewards: {mean_reward:0.4f} Episodes: {n_eval_episodes}\n"
    print(eval_str)

    with open(parameter_out_file_name, "a+") as parout:
        parout.write(eval_str)