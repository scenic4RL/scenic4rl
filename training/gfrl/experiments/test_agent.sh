#!/bin/bash

python3 -u -m gfrl.base.load_ppo2 \
  --eval_level ../_scenarios/academy/rts.scenic  \
  --reward_experiment scoring \
  --policy impala_cnn \
  --num_timesteps 1000 \
  --num_envs 2 \
  --nsteps 1024 \
  --exp_root ../_res \
  --exp_name pass_n_shoot \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res/rts_0/checkpoints/00006 \
  "$@"

# Needed to add: max_grad_norm

# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95

