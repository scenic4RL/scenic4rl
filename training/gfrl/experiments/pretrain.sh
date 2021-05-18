#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
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
  --exp_root ../_res_pretrain/ \
  --exp_name sc4rl_fg_11v1_on_rand_8K \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res_bc/bc_fg11v1_8K_rand1_success_1/checkpoints/bc_00126 \
  "$@"

python3 -u -m gfrl.base.run_my_ppo2 \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/ps_3v2_0.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/ps_3v2_0.scenic  \
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
  --exp_root ../_res_pretrain/ \
  --exp_name sc4rl_ps_3v2_0_on_rand_8K \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res_bc/bc_ps_3v2_0_rand_8K_success_1/checkpoints/bc_00125 \
  "$@"



