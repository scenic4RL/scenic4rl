#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/pass_n_shoot.scenic  \
  --eval_level ../_scenarios/academy/pass_n_shoot.scenic  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --cliprange 0.115 \
  --gamma 0.997 \
  --ent_coef 0.00155 \
  --num_timesteps 1000000 \
  --max_grad_norm 0.76 \
  --lr 0.00011879 \
  --num_envs 16 \
  --noptepochs 2 \
  --nminibatches 4 \
  --nsteps 512 \
  --save_interval 50 \
  --eval_interval 25 \
  --exp_root ../_res_pretrain/ \
  --exp_name pretrained_pass_n_shoot_from_rl_agent \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res_bc/bc_pass_n_shoot_RL_16k_b256_0/checkpoints/bc_00129 \
  "$@"
