from ray.rllib.env.multi_agent_env import MultiAgentEnv
from scenic.simulators.gfootball.rl.gfScenicEnv_v3 import GFScenicEnv_v3
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
import gym

class RllibGFootball(MultiAgentEnv):
    """An example of a wrapper for GFootball to make it compatible with rllib."""

    def __init__(self, scenario_file, player_control_mode, env_config=None):
        # self.env = football_env.create_environment(
        #     env_name='academy_pass_and_shoot_with_keeper', stacked=True,
        #     representation='extracted',
        #     logdir=os.path.join(tempfile.gettempdir(), 'rllib_test'),
        #     write_goal_dumps=False, write_full_episode_dumps=False, render=True,
        #     dump_frequency=0,
        #     number_of_left_players_agent_controls=num_agents,
        #     channel_dimensions=(42, 42)
        # )
        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring',
            "representation": 'extracted',
            # "real_time": True,
            "dump_frequency": 0,
            # "channel_dimensions": (42, 42)
        }
        scenario = buildScenario(scenario_file)

        # rank is used to discern env across workers
        # Notice env_config may appear empty {} but always contains worker_index
        rank = env_config.worker_index if env_config is not None else 100

        self.env = GFScenicEnv_v3(initial_scenario=scenario, player_control_mode=player_control_mode,
                                  gf_env_settings=gf_env_settings, allow_render=False, rank=rank)

        self.action_space = gym.spaces.Discrete(self.env.action_space.nvec[1])
        self.observation_space = gym.spaces.Box(
            low=self.env.observation_space.low[0],
            high=self.env.observation_space.high[0],
            dtype=self.env.observation_space.dtype)

        self.num_agents = self.env.num_left_controlled

    def reset(self):
        original_obs = self.env.reset()
        obs = {}
        for x in range(self.num_agents):
            if self.num_agents > 1:
                obs['agent_%d' % x] = original_obs[x]
            else:
                obs['agent_%d' % x] = original_obs
        return obs

    def step(self, action_dict):
        actions = []
        for key, value in sorted(action_dict.items()):
            actions.append(value)
        o, r, d, i = self.env.step(actions)
        rewards = {}
        obs = {}
        infos = {}
        for pos, key in enumerate(sorted(action_dict.keys())):
            infos[key] = i
            if self.num_agents > 1:
                rewards[key] = r[pos]
                obs[key] = o[pos]
            else:
                rewards[key] = r
                obs[key] = o
        dones = {'__all__': d}
        return obs, rewards, dones, infos
