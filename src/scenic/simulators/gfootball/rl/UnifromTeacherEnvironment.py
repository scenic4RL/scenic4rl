import random
import socket

import gym
from scenic.simulators.gfootball import rl_trainer
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
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


#TODO: add evaluation after each 50000 steps
#TODO: collect stat on environments


class UnifromTeacherEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, target_task, sub_tasks):
        all_tasks = [target_task] + sub_tasks

        self.target_task = buildScenario(target_task)
        self.sub_tasks = [buildScenario(task) for task in sub_tasks]

        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring,checkpoints',
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False,
            "action_set": "default"
        }

        from scenic.simulators.gfootball.rl_trainer import GFScenicEnv

        self.target_env = GFScenicEnv(initial_scenario=self.target_task, gf_env_settings=gf_env_settings)
        self.subtask_envs = [GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings) for scenario in self.sub_tasks]

        self.all_envs = [self.target_env] + self.subtask_envs
        self.current_env = self.target_env

        self.observation_space = self.target_env.observation_space
        self.action_space = self.target_env.action_space

        self.counts = {i:0 for i in range(len(self.all_envs))}

        """
        #assign name
        for i, task_path in enumerate(all_tasks):
            si = task_path.rfind("/") + 1
            ei = task_path.rfind(".")
            task_name = task_path[si:ei]
            self.all_envs[i].name = task_name
        """


    def step(self, action):
        return self.current_env.step(action)

    def reset(self):
        #Teacher Algorithm Here
        sel = random.randint(0, len(self.all_envs)-1)
        self.current_env = self.all_envs[sel]
        self.counts[sel]+=1
        #print(sel)

        return self.current_env.reset()

    def render(self, mode='human', close=False):
        return self.current_env.render(mode=mode, close=close)



if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    # scenario_file = f"{cwd}/academy/academy_run_pass_and_shoot_with_keeper.scenic"

    # n_task = 3

    target_task = f"{cwd}/exp_0_0/test_env.scenic"
    subtasks = [
        f"{cwd}/exp_0_0/test_env_2.scenic",
        f"{cwd}/exp_0_0/test_env_3.scenic"
    ]

    env = UnifromTeacherEnvironment(target_task, subtasks)
    rl_trainer.run_built_in_ai_game_with_rl_env(env, trials=15)
    #print(env.counts)