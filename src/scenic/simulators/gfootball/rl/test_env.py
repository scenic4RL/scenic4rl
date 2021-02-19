import socket


from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.policies import ActorCriticCnnPolicy
import os
import datetime
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import EvalCallback
# settings = scenario.settings

# env = gfootball.env.create_environment(env_name="11_vs_11_stochastic", stacked=True, representation='extracted', rewards="scoring,checkpoints")
# env2 = gfootball.env.create_environment(env_name="11_vs_11_stochastic", stacked=True, representation='extracted', rewards="scoring,checkpoints", other_config_options={"action_set":"v2"})
# run_built_in_ai_game_with_rl_env(env)
from stable_baselines3.common.vec_env import DummyVecEnv


class TestBasic:

    def __init__(self, scenario):

        self.scenario = scenario

        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring, checkpoints',
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False,
            "action_set": "default"
        }

        from scenic.simulators.gfootball.rl_trainer import GFScenicEnv
        self.rl_env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=False)

        #self.rl_env.eval_env = self.rl_env
        from scenic.simulators.gfootball.rl_trainer import run_built_in_ai_game_with_rl_env
        run_built_in_ai_game_with_rl_env(self.rl_env)


if __name__ == "__main__":
    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    scenario_file = f"{cwd}/exp_0_0/test_env.scenic"
    scenario = buildScenario(scenario_file)
    TestBasic(scenario)
