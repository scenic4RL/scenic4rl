from scenic.simulators.gfootball.rl_interface import GFScenicEnv
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario


def visualize_agent():
    from gfrl.common.my_sb.my_evaluation import evaluate_policy
    from gfrl.common import sb_utils
    import os


    gf_env_settings = {
        "stacked": True,
        "rewards": "scoring",
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": True,
        "action_set": "default",
        "dump_full_episodes": False,
        "dump_scores": False,
        "write_video": False,
        "tracesdir": "dummy",
        "write_full_episode_dumps": False,
        "write_goal_dumps": False,
        "render": False,
    }

    #eval_env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu=1, monitordir="../_exp/")
    #eval_env = VecTransposeImage(eval_env)

    #scenario_file = f"{os.getcwd()}/../_scenarios/academy/pass_n_shoot.scenic"
    scenario_file = f"{os.getcwd()}/../_scenarios/academy/run_pass_shoot.scenic"

    scenario = buildScenario(scenario_file)
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True)
    #env = VecTransposeImage(DummyVecEnv([env]))
    model = PPO.load("/Users/azadsalam/Downloads/eval/model_100000")

    n_trials = 2
    for _ in range(n_trials):
        done = False
        o = env.reset()
        while not done:
            action = model.predict(o, deterministic=True)[0]
            o,_,done,_ = env.step(action)



    #print(evaluate_policy(model, eval_env, n_eval_episodes=5))

def evalutate_agent(env, model, n_trials):
    from gfrl.common.my_sb.my_evaluation import evaluate_policy
    from gfrl.common import sb_utils
    import os
    scenario_file = f"{os.getcwd()}/../_scenarios/exp/pass_n_shoot.scenic"

    gf_env_settings = {
        "stacked": True,
        "rewards": "scoring",
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default",
        "dump_full_episodes": False,
        "dump_scores": False,
        "write_video": False,
        "tracesdir": "dummy",
        "write_full_episode_dumps": False,
        "write_goal_dumps": False,
        "render": False
    }

    eval_env = sb_utils.get_vecenv_from_scenario(scenario_file, gf_env_settings, num_cpu=1, monitordir="../_exp/")
    eval_env = VecTransposeImage(eval_env)

    model = PPO.load("/Users/azadsalam/codebase/scenic/training/gfrl/_exp/dev_0/eval/best_model.zip")
    print(evaluate_policy(model, eval_env, n_eval_episodes=5))


from gfrl.common.my_sb.ppo import PPO
from stable_baselines3.common.vec_env import VecTransposeImage, DummyVecEnv

if __name__ == "__main__":

    visualize_agent()


