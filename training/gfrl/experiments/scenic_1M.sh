#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/sc4rl/ps_3v2_1.scenic  \
  --eval_level ../_scenarios/sc4rl/ps_3v2_1.scenic  \
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
  --save_interval 10 \
  --eval_interval 10 \
  --exp_root ../_resv2/sc4rl1M \
  --exp_name pass_3v2_1 \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/sc4rl/fg_11v1.scenic  \
  --eval_level ../_scenarios/sc4rl/fg_11v1.scenic  \
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
  --save_interval 10 \
  --eval_interval 10 \
  --exp_root ../_resv2/sc4rl1M \
  --exp_name fg_11v1_v0 \
  "$@"

python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/sc4rl/tp_3v3_v0.scenic  \
  --eval_level ../_scenarios/sc4rl/tp_3v3_v0.scenic  \
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
  --save_interval 10 \
  --eval_interval 10 \
  --exp_root ../_resv2/sc4rl1M \
  --exp_name pass_3v2_0 \
  "$@"

python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/sc4rl/rs_3v3_v0.scenic  \
  --eval_level ../_scenarios/sc4rl/rs_3v3_v0.scenic  \
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
  --save_interval 10 \
  --eval_interval 10 \
  --exp_root ../_resv2/sc4rl1M \
  --exp_name run_shoot_3v3_v0 \
  "$@"

python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/sc4rl/ps_3v2_0.scenic  \
  --eval_level ../_scenarios/sc4rl/ps_3v2_0.scenic  \
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
  --exp_root ../_resv2/sc4rl5M \
  --exp_name pass_3v2_0 \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/sc4rl/ps_3v2_1.scenic  \
  --eval_level ../_scenarios/sc4rl/ps_3v2_1.scenic  \
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
  --exp_root ../_resv2/sc4rl5M \
  --exp_name pass_3v2_1 \
  "$@"