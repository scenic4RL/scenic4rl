python3 -u -m gfrl.base.run_bc \
  --level ../_scenarios/academy/easy_counter.scenic  \
  --eval_level ../_scenarios/academy/easy_counter.scenic  \
  --dataset /home/ubuntu/ScenicGFootBall/training/gfrl/_data/pns_50.npz  \
  --reward_experiment scoring \
  --policy gfootball_impala_cnn \
  --lr 3e-4 \
  --n_epochs 2 \
  --batch_size 64 \
  --save_interval 0 \
  --eval_timesteps 400 \
  --eval_interval 3 \
  --exp_root ../_res_bc \
  --exp_name bc_easy_counter \
  "$@"

# Needed to add: max_grad_norm

# Good but unsettable defaults:
# Optimizer: adam
# Value-function coefficient is 0.5
# GAE (lam): 0.95



