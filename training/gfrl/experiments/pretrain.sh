#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
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
  --eval_interval 10 \
  --exp_root ../_res_pretrain/ \
  --exp_name sc4rl_fg_11v1_on_rs_rand1_8K \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res_bc/bc_fg11v1_10K_rand1_success_2/checkpoints/bc_00063 \
  "$@"

  python3 -u -m gfrl.base.run_my_ppo2 \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/fg_11v1.scenic  \
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
  --eval_interval 10 \
  --exp_root ../_res_pretrain/ \
  --exp_name sc4rl_fg_11v1_on_rs_8K \
  --load_path /home/ubuntu/ScenicGFootBall/training/gfrl/_res_bc/bc_fg11v1_10K_success_2/checkpoints/bc_00062 \
  "$@"
