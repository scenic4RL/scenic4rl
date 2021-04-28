python3 -u -m gfrl.base.run_bc \
  --level ../_scenarios/academy/pass_n_shoot.scenic  \
  --eval_level ../_scenarios/academy/pass_n_shoot.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/pns_success_10000.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 10 \
  --batch_size 512 \
  --save_interval  50 \
  --eval_timesteps 800 \
  --eval_interval  5 \
  --exp_root ../_res_bc \
  --exp_name bc_pass_n_shoot_10K_success_b512_epoch_10 \
  "$@"
