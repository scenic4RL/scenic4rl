#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/attack/cross_easy.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/attack/cross_easy.scenic  \
  --env_mode v1 \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --cliprange 0.115 \
  --gamma 0.997 \
  --ent_coef 0.00155 \
  --num_timesteps 5000000 \
  --max_grad_norm 0.76 \
  --lr 0.00011879 \
  --num_envs 16 \
  --noptepochs 2 \
  --nminibatches 4 \
  --nsteps 512 \
  --save_interval 50 \
  --eval_interval 50 \
  --exp_root ../_res_v3/sc4rl5M \
  --exp_name cross_easy \
  "$@"


