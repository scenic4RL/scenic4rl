from gfrl.base.run_my_ppo2 import create_single_scenic_environment
import numpy as np
from baselines.common.runners import AbstractEnvRunner

class MyTrajRunner(AbstractEnvRunner):
    """
    We use this object to make a mini batch of experiences
    __init__:
    - Initialize the runner
    run():
    - Make a mini batch
    """
    def __init__(self, *, env, model, nsteps, num_episodes):
        super().__init__(env=env, model=model, nsteps=nsteps)
        self.num_episodes = num_episodes

        from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
        assert isinstance(env, DummyVecEnv), "Only works with Dummy Vec Env"
        assert len(self.env.envs)==1, "Only works with Dummy Vec Env with 1 envs"

    def run(self):
        print("in run")
        # Here, we init the lists that will contain the mb of experiences
        mb_obs, mb_rewards, mb_actions, mb_values, mb_dones, mb_neglogpacs = [],[],[],[],[],[]
        mb_gt = []
        mb_states = self.states
        epinfos = []
        # For n in range number of steps
        epi_passed = 0 
              
        while epi_passed<self.num_episodes:

            # Given observations, get action value and neglopacs
            # We already have self.obs because Runner superclass run self.obs[:] = env.reset() on init
            mb_gt.append(self.env.envs[0].simulation.last_raw_obs) 
            actions, values, self.states, neglogpacs = self.model.step(self.obs, S=self.states, M=self.dones)
            mb_obs.append(self.obs.copy())
            mb_actions.append(actions)
            mb_values.append(values)
            mb_neglogpacs.append(neglogpacs)
            mb_dones.append(self.dones)
            

            # Take actions in env and look the results
            # Infos contains a ton of useful informations
            self.obs[:], rewards, self.dones, infos = self.env.step(actions)
            
            if self.dones[0]: 
                epi_passed+=1 
                #print(self.dones[0], rewards, len(mb_gt), len(mb_obs), len(mb_actions),infos)

            for info in infos:
                maybeepinfo = info.get('episode')
                if maybeepinfo: epinfos.append(maybeepinfo)
            mb_rewards.append(rewards)

        #batch of steps to batch of rollouts
        mb_obs = np.asarray(mb_obs, dtype=self.obs.dtype)
        mb_rewards = np.asarray(mb_rewards, dtype=np.float32)
        mb_actions = np.asarray(mb_actions)
        mb_values = np.asarray(mb_values, dtype=np.float32)
        mb_neglogpacs = np.asarray(mb_neglogpacs, dtype=np.float32)
        mb_dones = np.asarray(mb_dones, dtype=np.bool)
        last_values = self.model.value(self.obs, S=self.states, M=self.dones)

        return (*map(sf01, (mb_obs, mb_rewards, mb_dones, mb_actions, mb_values, mb_neglogpacs)),
            mb_states, epinfos, mb_gt)



# obs, returns, masks, actions, values, neglogpacs, states = runner.run()
def sf01(arr):
    """
    swap and then flatten axes 0 and 1
    """
    s = arr.shape
    return arr.swapaxes(0, 1).reshape(s[0] * s[1], *s[2:])



if __name__=="__main__":
    scenario = "../_scenarios/academy/3v1.scenic"

    from baselines.common.vec_env.subproc_vec_env import SubprocVecEnv

    from baselines.common.vec_env.dummy_vec_env import DummyVecEnv

    """
    vec_env = SubprocVecEnv([lambda _i=i: \
                            create_single_scenic_environment(_i,scenario) for i in
                            range(2)], context=None)
    """


    dummy_vec_env = DummyVecEnv([lambda _i=i: \
                            create_single_scenic_environment(_i,scenario) for i in
                            range(1)])

    print("ENV CREATED")

    import tensorflow.compat.v1 as tf
    import multiprocessing
    #import tensorflow as tf

    ncpu = multiprocessing.cpu_count()
    config = tf.ConfigProto(allow_soft_placement=True,
                            intra_op_parallelism_threads=ncpu,
                            inter_op_parallelism_threads=ncpu)
    config.gpu_options.allow_growth = True
    tf.Session(config=config).__enter__()


    network = "gfootball_impala_cnn"

    from gfrl.common.mybase import ppo2
    model = ppo2.learn(
        network=network,
        total_timesteps=0,
        env=dummy_vec_env,
        nsteps=512,
        load_path="/home/ubuntu/ScenicGFootBall/training/gfrl/_saved_models/3v1_5M/final_00610",
        )


    print("Model Loaded")

    print("before runner")
    #quit()

    dummy_vec_env = DummyVecEnv([lambda _i=i: \
                            create_single_scenic_environment(_i,scenario) for i in
                            range(1)])


    print("ENV CREATED AGAIN")
    runner = MyTrajRunner(env=dummy_vec_env, model=model, nsteps=128, num_episodes=2)
    print("runner init")



    mb_obs, mb_rewards, mb_dones, mb_actions, mb_values, mb_neglogpacs, mb_states, epinfos, mb_gt = runner.run()

    print(mb_obs.shape, mb_dones.shape)
