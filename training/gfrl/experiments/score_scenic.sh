#!/bin/bash

python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/rts_with_keeper.scenic  \
  --eval_level ../_scenarios/academy/rts_with_keeper.scenic  \
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
  --eval_interval  5 \
  --exp_root ../_academy_1M \
  --exp_name rts_with_keeper \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/3v1.scenic  \
  --eval_level ../_scenarios/academy/3v1.scenic  \
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
  --eval_interval  5 \
  --exp_root ../_academy_1M \
  --exp_name 3v1 \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/easy_counter.scenic  \
  --eval_level ../_scenarios/academy/easy_counter.scenic  \
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
  --eval_interval  5 \
  --exp_root ../_academy_1M \
  --exp_name easy_counter \
  "$@"


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
  --save_interval 10 \
  --eval_interval  5 \
  --exp_root ../_academy_1M \
  --exp_name pass_n_shoot \
  "$@"



python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/rts.scenic  \
  --eval_level ../_scenarios/academy/rts.scenic  \
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
  --eval_interval  5 \
  --exp_root ../_academy_1M \
  --exp_name rts \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/run_pass_shoot.scenic  \
  --eval_level ../_scenarios/academy/run_pass_shoot.scenic  \
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
  --eval_interval  5 \
  --exp_root ../_academy_1M \
  --exp_name run_pass_shoot \
  "$@"


python3 -u -m gfrl.base.run_my_ppo2 \
  --level ../_scenarios/academy/rts_with_keeper.scenic  \
  --eval_level ../_scenarios/academy/rts_with_keeper.scenic  \
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
  --eval_interval 25 \
  --exp_root ../_academy_5M \
  --exp_name rts_with_keeper \
  "$@"



# Needed to add: max_grad_norm

# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95

