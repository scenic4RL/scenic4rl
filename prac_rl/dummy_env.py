import numpy as np
import gym


class DummyGFEnv(gym.Env):
    def __init__(self):
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(72, 96, 16), dtype=np.uint8)
        self.action_space = gym.spaces.discrete.Discrete(19)

    def reset(self):
        return np.zeros((72,96,16), dtype=np.uint8)

    def step(self, action):
        return np.zeros((72,96,16), dtype=np.uint8), 0, False, {}


if __name__=="__main__":

    env = DummyGFEnv()

    o = env.reset()
    for _ in range(100):
        o,r,d,i = env.step([0])


