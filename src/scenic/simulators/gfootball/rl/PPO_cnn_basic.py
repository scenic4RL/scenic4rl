import socket
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.policies import ActorCriticCnnPolicy
import os
import datetime


# settings = scenario.settings

# env = gfootball.env.create_environment(env_name="11_vs_11_stochastic", stacked=True, representation='extracted', rewards="scoring,checkpoints")
# env2 = gfootball.env.create_environment(env_name="11_vs_11_stochastic", stacked=True, representation='extracted', rewards="scoring,checkpoints", other_config_options={"action_set":"v2"})
# run_built_in_ai_game_with_rl_env(env)

class PPOScenicBasic:

    def __init__(self, scenario):

        self.scenario = scenario

        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring,checkpoints',
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False
        }

        from scenic.simulators.gfootball.rl_trainer import GFScenicEnv
        self.rl_env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
        # run_built_in_ai_game_with_rl_env(rl_env)
        # pfrl_training.pfrl_training(rl_env)


    def train(self):
        ALGO = PPO
        n_eval_episodes = 10
        total_training_timesteps = 100000
        save_dir = "./saved_models"
        logdir = "./tboard"

        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(logdir, exist_ok=True)

        env = self.rl_env
        env = Monitor(env)

        model = ALGO("CnnPolicy", env, verbose=1, tensorboard_log=logdir)


        currentDT = datetime.datetime.now()
        fstr = f"HM_{currentDT.hour}_{currentDT.minute}__DM_{currentDT.day}_{currentDT.month}"
        model.learn(total_timesteps=total_training_timesteps, tb_log_name=f"{socket.gethostname()}_{fstr}")

        model.save(f"{save_dir}/PPO_basic_{total_training_timesteps}")

        mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=n_eval_episodes)
        print(f"Eval Mean Rewards: {mean_reward:0.4f} Episodes: {n_eval_episodes}")



if __name__ == "__main__":
    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    scenario_file = f"{cwd}/exp_0_0/academy_run_pass_and_shoot_with_keeper.scenic"
    scenario = buildScenario(scenario_file)
    PPOScenicBasic(scenario).train()
