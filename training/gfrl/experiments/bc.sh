python3 -u -m gfrl.base.run_bc \
  --level ../_scenarios/academy/pass_n_shoot.scenic  \
  --eval_level ../_scenarios/academy/pass_n_shoot.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/pns_rl_500.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 2 \
  --batch_size 256 \
  --save_interval  50 \
  --eval_timesteps 500 \
  --eval_interval  1 \
  --exp_root ../_res_bc \
  --exp_name bc_pass_n_shoot_RL_16k_b256 \
  "$@"


