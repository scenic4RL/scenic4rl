#!/bin/bash

python3 -u -m gfrl.base.evaluate_ppo2 \
  --eval_level ../_scenarios/generic/rts/gen_0.scenic  \
  --reward_experiment scoring \
  --policy impala_cnn \
  --num_timesteps 1000 \
  --num_envs 16 \
  --nsteps 1024 \
  --exp_root ../_test_res \
  --exp_name rps \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res/generic_rts_0/checkpoints/final_00061 \
  "$@"

#--eval_level ../_scenarios/generic/rts/gen_0.scenic  \
#--eval_level ../_scenarios/academy/rts.scenic  \
#--load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res/rts_2/checkpoints/00060 \ 
#--load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res/rts_1/checkpoints/00060 \

# Needed to add: max_grad_norm

# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95

