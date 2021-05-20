#!/bin/bash

python3 -u -m gfrl.base.evaluate_ppo2 \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/ps_3v2_0.scenic \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_saved_models/ps_3v2_0/final_00610 \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --num_timesteps 0 \
  --num_envs 16 \
  --nsteps 1600 \
  --exp_root ../_test_res \
  --exp_name rps \
  "$@"

#/home/ubuntu/ScenicGFootBall/training/gfrl/_res_latest/generic_rts_4/checkpoints/final_00122
#/home/ubuntu/ScenicGFootBall/training/gfrl/_res_latest/rts_5/checkpoints/final_00122
#$--load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res_latest/rts_5/checkpoints/final_00122 \ 
#--load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res/final_00061 \


#--eval_level ../_scenarios/generic/rts/gen_0.scenic  \
#--eval_level ../_scenarios/academy/rts.scenic  \


# Needed to add: max_grad_norm

# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95

