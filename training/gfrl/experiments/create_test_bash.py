import os
from textwrap import dedent


def add_test(name, level_path, load_path):    
    return dedent(f"""python3 -u -m gfrl.base.evaluate_ppo2 \
  --eval_level {level_path} \
  --nsteps 800 \
  --env_mode v2 \
  --load_path {load_path} \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --num_timesteps 0 \
  --num_envs 14 \
  --exp_root ../_test_aaai \
  --exp_name {name} \
  "$@"
  """)

  


def create_test(name, level_path, load_path, start, end):
    assert os.path.exists(level_path)
    res = []
    for i in range(start, end):
        assert "$" in load_path
        actual_path = load_path.replace("$", str(i))
        assert os.path.exists(actual_path)

        each_name = f"{name}{i}"
        res.append(add_test(each_name, level_path, actual_path))
    return res


if __name__ == '__main__':

    
    '''
    Entry Format: (name, level_path, load_path, start (inclusive), end (exclusive))
    1. For load_path, change the counter in the folder name to symbol $. Example: offense_11v1_0 -> offense_11v1_$
    The code will replace it with counter i in (start, end]
    2. Make sure to choose a descriptive name. The testing result is stored with this name in the csv file. 
    3. The code checks if all the provided path exists.
    '''
    params_all = [
        ["offense_on_test_",
         "/home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/testing_generalization/offense_avoid_pass_shoot.scenic",
         "/home/ubuntu/ScenicGFootBall/ppo/offense/avoid_pass_shoot_$/checkpoints/final_00610", 0, 10],
        ["offense_on_test_",
         "/home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/testing_generalization/offense_easy_crossing.scenic",
         "/home/ubuntu/ScenicGFootBall/ppo/offense/cross_easy_$/checkpoints/final_00610", 0, 10],
        ["offense_on_test_",
         "/home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/testing_generalization/offense_hard_crossing.scenic",
         "/home/ubuntu/ScenicGFootBall/ppo/offense/cross_hard_$/checkpoints/final_00610", 0, 10],
    ]

    with open("evaluate_offense_on_test.bash", "w") as f:
        f.write("#!/bin/bash\n")
        # for p in params_old:
        #     actual_p = [p[0], p[1], p[2], 0, 2]
        #     f.writelines(create_test(*actual_p))
        # for p in params_new:
        #     actual_p = [p[0], p[1], p[2], 0, 8]
        #     f.writelines(create_test(*actual_p))
        for p in params_all:
            f.writelines(create_test(*p))

    print("Done.")