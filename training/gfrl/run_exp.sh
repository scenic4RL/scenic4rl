#!/bin/bash
#OPENAI_LOG_FORMAT="stdout,tensorboard,log,csv"
python3 -u -m run_my_ppo2 \
  --level 11_vs_11_easy_stochastic \
  --reward_experiment scoring \
  --policy impala_cnn \
  --cliprange 0.115 \
  --gamma 0.997 \
  --ent_coef 0.00155 \
  --num_timesteps 10000 \
  --max_grad_norm 0.76 \
  --lr 0.00011879 \
  --num_envs 12 \
  --noptepochs 2 \
  --nminibatches 8 \
  --nsteps 512 \
  --save_interval 2 \
  --exp_root _res \
  --exp_name dev \
  "$@"


# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95
