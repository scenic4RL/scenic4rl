import random
import socket

import gym
from scenic.simulators.gfootball import rl_interface
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.policies import ActorCriticCnnPolicy
import os
import datetime


class UnifromTeacherEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, target_task, sub_tasks, gf_env_settings, rank = 0, allow_render = False):
        #all_tasks = [target_task] + sub_tasks

        self.target_task = buildScenario(target_task)
        self.sub_tasks = [buildScenario(task) for task in sub_tasks]
        self.sub_task_names = [task[task.rfind("/")+1: task.rfind(".")] for task in sub_tasks]
        self.task_name = target_task[target_task.rfind("/")+1: target_task.rfind(".")]
        #self.use_checkpoint_reward = use_checkpoint_reward
        #if use_checkpoint_reward: rewards = "scoring,checkpoints"
        #else: rewards = "scoring"


        from scenic.simulators.gfootball.rl_interface import GFScenicEnv

        self.target_env = GFScenicEnv(initial_scenario=self.target_task, gf_env_settings=gf_env_settings, allow_render=allow_render, rank=rank)
        self.subtask_envs = [GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=allow_render, rank=rank) for scenario in self.sub_tasks]

        self.all_envs = [self.target_env] + self.subtask_envs
        self.task_names = [self.task_name] + self.sub_task_names
        self.current_env = self.target_env

        self.observation_space = self.target_env.observation_space
        self.action_space = self.target_env.action_space

        self.counts = {i:0 for i in range(len(self.all_envs))}
        self.evaluation = False


    def step(self, action):
        o, r, d, i = self.current_env.step(action)
        i["task_name"] = self.task_names[self.current_env_idx]
        return o, r, d, i

    def reset(self):
        #Teacher Algorithm Here
        if self.evaluation:
            sel = 0
        else:
            sel = random.randint(0, len(self.all_envs)-1)

        self.current_env_idx = sel
        self.current_env = self.all_envs[sel]
        self.counts[sel]+=1
        #print("Evaluation Status? ", self.evaluation, "Selected Env", sel)

        return self.current_env.reset()

    def set_evalautaion_status(self, status:bool):
        self.evaluation=status
        #print(f"setting evaluation status: {self.evaluation}")

    def render(self, mode='human', close=False):
        return self.current_env.render(mode=mode, close=close)



if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring',
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default"
    }

    # scenario_file = f"{cwd}/academy/academy_run_pass_and_shoot_with_keeper.scenic"

    # n_task = 3

    target_task = f"{cwd}/../_scenarios/uniform/rtsk0/rts_with_keeper.scenic"
    subtasks = [
        f"{cwd}/../_scenarios/uniform/rtsk0/sub0.scenic",
        f"{cwd}/../_scenarios/uniform/rtsk0/sub1.scenic",
        f"{cwd}/../_scenarios/uniform/rtsk0/sub2.scenic",
        f"{cwd}/../_scenarios/uniform/rtsk0/sub3.scenic",
    ]

    env = UnifromTeacherEnvironment(target_task, subtasks, gf_env_settings)
    rl_interface.run_built_in_ai_game_with_rl_env(env, trials=20)
    #print(env.counts)