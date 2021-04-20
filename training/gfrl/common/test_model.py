from scenic.simulators.gfootball.rl_interface import GFScenicEnv
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario





def evalutate_random_policy(n_trials):
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

    scenario = buildScenario(scenario_file)
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, rank=rank)

    rews=[]
    for _ in range(n_trials):
        done = False
        rew = 0
        o = env.reset()
        while not done:
            action = env.action_space.sample()
            o,r,done,_ = env.step(action)
            rew += r 

        rews.append(rew)

    print(rews)



def evalutate_agent(env, model, n_trials):

    import os
    scenario_file = f"{os.getcwd()}/../_scenarios/exp/pass_n_shoot.scenic"


    from gfrl.base.run_my_ppo2 import create_single_scenic_environment

    env = create_single_scenic_environment(0, scenario_file)

    from gfrl.common.mybase import ppo2

    ppo2 = ppo2.learn(
        network="impala_cnn",
        total_timesteps=FLAGS.num_timesteps,
        env=vec_env,
        eval_env = eval_env,
        seed=FLAGS.seed,
        nsteps=FLAGS.nsteps,
        nminibatches=FLAGS.nminibatches,
        noptepochs=FLAGS.noptepochs,
        max_grad_norm=FLAGS.max_grad_norm,
        gamma=FLAGS.gamma,
        ent_coef=FLAGS.ent_coef,
        lr=FLAGS.lr,
        log_interval=1,
        eval_interval=FLAGS.eval_interval,
        save_interval=FLAGS.save_interval,
        cliprange=FLAGS.cliprange,
        load_path=FLAGS.load_path
        )

    



    for _ in range(n_trials):
        obs, done = env.reset(), False
        episode_rew = 0
        while not done:
            env.render()
            obs, rew, done, _ = env.step(act(obs[None])[0])
            episode_rew += rew
        print("Episode reward", episode_rew)



if __name__ == "__main__":

    #visualize_agent()
    #evalutate_random_policy(5)
    evalutate_agent("", "", 5)


