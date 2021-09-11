#!/bin/bash

python3 -u -m gfrl.base.run_bc \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/offense/avoid_pass_shoot.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/offense/avoid_pass_shoot.scenic  \
  --env_mode v2  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_demonstration_data/offense_avoid_pass_shoot.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 5 \
  --batch_size 256 \
  --save_interval  50 \
  --eval_timesteps 800 \
  --eval_interval  1 \
  --exp_root ../_res_bc \
  --exp_name offense_avoid_pass_shoot \
  "$@"
