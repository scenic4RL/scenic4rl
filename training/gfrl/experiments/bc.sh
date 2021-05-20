#!/bin/bash

python3 -u -m gfrl.base.run_bc \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/sc4rl_fg11v1_rns_rand1_succ_10000.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 4 \
  --batch_size 256 \
  --save_interval  50 \
  --eval_timesteps 800 \
  --eval_interval  1 \
  --exp_root ../_res_bc \
  --exp_name bc_fg11v1_8K_rand1_success \
  "$@"


: '
python3 -u -m gfrl.base.run_bc \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/ps_3v2_0.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/ps_3v2_0.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/sc4rl_ps_3v2_0_v0_rand0_10000.npz \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 4 \
  --batch_size 256 \
  --save_interval  50 \
  --eval_timesteps 800 \
  --eval_interval  1 \
  --exp_root ../_res_bc \
  --exp_name bc_ps_3v2_0_rand_8K_success \
  "$@"

python3 -u -m gfrl.base.run_bc \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/sc4rl_fg11v1_rns_rand1_succ_10000.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 2 \
  --batch_size 256 \
  --save_interval  50 \
  --eval_timesteps 800 \
  --eval_interval  1 \
  --exp_root ../_res_bc \
  --exp_name bc_fg11v1_10K_rand1_success \
  "$@"
'