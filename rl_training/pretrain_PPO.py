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


class ExpertDataSet(Dataset):
    def __init__(self, expert_observations, expert_actions):
        self.observations = expert_observations
        self.actions = expert_actions

    def __getitem__(self, index):
        return (self.observations[index], self.actions[index])

    def __len__(self):
        return len(self.observations)

def pretrain_agent(
        student,
        env,
        expert_dataset,
        batch_size=64,
        epochs=10,
        scheduler_gamma=0.7,
        learning_rate=1.0,
        log_interval=100,
        no_cuda=True,
        seed=1,
        test_batch_size=64,
):
    train_size = int(0.8 * len(expert_dataset))

    test_size = len(expert_dataset) - train_size

    train_expert_dataset, test_expert_dataset = random_split(
        expert_dataset, [train_size, test_size]
    )

    print("test_expert_dataset: ", len(test_expert_dataset))
    print("train_expert_dataset: ", len(train_expert_dataset))


    use_cuda = not no_cuda and th.cuda.is_available()
    th.manual_seed(seed)
    device = th.device("cuda" if use_cuda else "cpu")
    kwargs = {"num_workers": 1, "pin_memory": True} if use_cuda else {}

    if isinstance(env.action_space, gym.spaces.Box):
        criterion = nn.MSELoss()
    else:
        criterion = nn.CrossEntropyLoss()

    # Extract initial policy
    model = student.policy.to(device)

    def train(model, device, train_loader, optimizer):
        model.train()

        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()

            if isinstance(env.action_space, gym.spaces.Box):
                # A2C/PPO policy outputs actions, values, log_prob
                # SAC/TD3 policy outputs actions only
                if isinstance(student, (A2C, PPO)):
                    action, _, _ = model(data)
                else:
                    # SAC/TD3:
                    action = model(data)
                action_prediction = action.double()
            else:
                # Retrieve the logits for A2C/PPO when using discrete actions
                latent_pi, _, _ = model._get_latent(data)
                logits = model.action_net(latent_pi)
                action_prediction = logits
                target = target.long()

            loss = criterion(action_prediction, target)
            loss.backward()
            optimizer.step()
            if batch_idx % log_interval == 0:
                print(
                    "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                        epoch,
                        batch_idx * len(data),
                        len(train_loader.dataset),
                        100.0 * batch_idx / len(train_loader),
                        loss.item(),
                    )
                )

    def test(model, device, test_loader):
        model.eval()
        test_loss = 0
        with th.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)

                if isinstance(env.action_space, gym.spaces.Box):
                    # A2C/PPO policy outputs actions, values, log_prob
                    # SAC/TD3 policy outputs actions only
                    if isinstance(student, (A2C, PPO)):
                        action, _, _ = model(data)
                    else:
                        # SAC/TD3:
                        action = model(data)
                    action_prediction = action.double()
                else:
                    # Retrieve the logits for A2C/PPO when using discrete actions
                    latent_pi, _, _ = model._get_latent(data)
                    logits = model.action_net(latent_pi)
                    action_prediction = logits
                    target = target.long()

                test_loss = criterion(action_prediction, target)
        test_loss /= len(test_loader.dataset)
        print(f"Test set: Average loss: {test_loss:.4f}")

    # Here, we use PyTorch `DataLoader` to our load previously created `ExpertDataset` for training
    # and testing
    train_loader = th.utils.data.DataLoader(
        dataset=train_expert_dataset, batch_size=batch_size, shuffle=True, **kwargs
    )
    test_loader = th.utils.data.DataLoader(
        dataset=test_expert_dataset, batch_size=test_batch_size, shuffle=True, **kwargs,
    )

    # Define an Optimizer and a learning rate schedule.
    optimizer = optim.Adadelta(model.parameters(), lr=learning_rate)
    scheduler = StepLR(optimizer, step_size=1, gamma=scheduler_gamma)

    # Now we are finally ready to train the policy model.
    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, optimizer)
        test(model, device, test_loader)
        scheduler.step()

    # Implant the trained policy network back into the RL student agent
    student.policy = model

def test_model_performance(env, model, num_trials=1):

    obs = env.reset()
    #env.render()
    num_epi = 0
    total_r = 0
    from tqdm import tqdm
    for i in tqdm(range(0, num_trials)):

        done = False

        while not done:
            action = model.predict(obs, deterministic=True)[0]
            obs, reward, done, info = env.step(action)
            #env.render()
            total_r+=reward
            if done:
                obs = env.reset()
                num_epi +=1

    return total_r/num_epi


def train(scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, tracedir, rewards, override_params={}, dump_traj=False, write_video=False):
    gf_env_settings = {
        "stacked": True,
        "rewards": rewards,
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default",
        "dump_full_episodes": dump_traj,
        "dump_scores": dump_traj,
        "write_video": write_video,
        "tracesdir": tracedir, 
        "write_full_episode_dumps": dump_traj,
        "write_goal_dumps": dump_traj,
        "render": write_video
    }
    #write_full_episode_dumps maybe redundant

    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    scenario = buildScenario(scenario_name)

    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
    features_extractor_class = GfootballImpalaCNN


    #get the PPO object with required parameters
    model, parameter_dict = pretrain_template.get_model_and_params(
        env=env, ALGO=PPO, features_extractor_class = features_extractor_class, scenario_name=scenario_name,
        logdir=logdir, override_params=override_params, rewards=rewards)


    print("env (from model) observation space: ", model.get_env().observation_space)



    #Load Expert data for now as proxy to expert data
    import os
    cwd = os.getcwd()
    loaded_data = np.load(f"{cwd}/pretrain/expert_data_20000.npz")

    expert_observations = loaded_data["expert_observations"]
    expert_actions = loaded_data["expert_actions"]
    print(f"Loaded data obs: {expert_observations.shape}, actions: {expert_actions.shape}")

    #pretrain the model now
    expert_dataset = ExpertDataSet(expert_observations, expert_actions)
    pretrain_agent(
        student=model,
        env=env,
        expert_dataset=expert_dataset,
        epochs=2
    )

    print("")
    print("Behavior Cloning Performance: ",  test_model_performance(env, model, num_trials=5))

    pretrain_template.train(model=model, parameters=parameter_dict,
                            n_eval_episodes=n_eval_episodes, total_training_timesteps=total_training_timesteps,
                            eval_freq=eval_freq,
                            save_dir=save_dir, logdir=logdir, dump_info={"rewards": rewards})



if __name__ == "__main__":

    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    scenario_file = f"{cwd}/exp_0_4/academy_run_to_score.scenic"
    n_eval_episodes = 10
    total_training_timesteps = 2000
    eval_freq = 5000

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard/dev"
    tracedir = f"{cwd}/game_trace"
    rewards = "scoring"#'scoring,checkpoints'
    
    print("model, tf logs, game trace are saved in: ", save_dir, logdir, tracedir)

    param_list = [
        {"n_steps": 4096},
    ]

    for override_params in param_list:
        train(scenario_name=scenario_file, n_eval_episodes = n_eval_episodes,
                        total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
                        save_dir=save_dir, logdir=logdir, tracedir=tracedir, rewards=rewards, override_params=override_params,
                        dump_traj=False, write_video=False)

