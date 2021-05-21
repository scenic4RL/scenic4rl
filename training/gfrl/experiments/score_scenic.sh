#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/wb/defense_1vs1_gk_wb.scenic  \
  --eval_level /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/wb/defense_1vs1_gk_wb.scenic  \
  --env_mode v2 \
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
  --exp_name defense_1vs1_idle_keeper_env_v2 \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level  /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/wb/defense_counterattack_3vs2_idle_gk.scenic  \
  --eval_level   /home/ubuntu/ScenicGFootBall/training/gfrl/_scenarios/sc4rl/wb/defense_counterattack_3vs2_idle_gk.scenic  \
  --env_mode v2 \
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
  --exp_name defense_counterattack_3vs2_idle_gk_env_v2 \
  "$@"


