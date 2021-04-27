python3 -u -m gfrl.base.run_bc \
  --level ../_scenarios/academy/pass_n_shoot.scenic  \
  --eval_level ../_scenarios/academy/pass_n_shoot.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/pns_10000.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 25 \
  --batch_size 512 \
  --save_interval  50 \
  --eval_timesteps 800 \
  --eval_interval  40 \
  --exp_root ../_res_bc \
  --exp_name bc_pass_n_shoot_10000 \
  "$@"

# Needed to add: max_grad_norm

# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95



