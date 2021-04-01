from torch.utils.data.dataset import Dataset, random_split
import numpy as np
class ExpertDataSet(Dataset):
    def __init__(self, expert_observations, expert_actions):
        self.observations = expert_observations
        self.actions = expert_actions

    def __getitem__(self, index):
        return (self.observations[index], self.actions[index])

    def __len__(self):
        return len(self.observations)
    
    
def mean_perf_random_agent(env, num_trials=1):

    obs = env.reset()
    #env.render()
    num_epi = 0
    all_rewards = []
    from tqdm import tqdm
    for i in tqdm(range(0, num_trials)):

        done = False
        total_r = 0
        while not done:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            #env.render()
            total_r+=reward
            if done:
                obs = env.reset()
                all_rewards.append(total_r)
                total_r=0
                num_epi +=1
                
    all_rewards = np.array(all_rewards)
    return np.mean(all_rewards), np.std(all_rewards)
    
    
def mean_perf_agent(agent, env, num_trials=5):
    
    #env.render()
    num_epi = 0
    all_rewards = []
    from tqdm import tqdm
    for i in tqdm(range(0, num_trials)):

        done = False
        total_r = 0
        obs = env.reset()
        while not done:
            action = agent.predict(obs, deterministic=True)[0]
            obs, reward, done, info = env.step(action)
            #env.render()
            total_r+=reward
            if done:
                all_rewards.append(total_r)
                num_epi +=1 
                
    all_rewards = np.array(all_rewards)
    return np.mean(all_rewards), np.std(all_rewards)
  
    
