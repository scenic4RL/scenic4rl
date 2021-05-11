def mean_reward_random_agent(env, num_trials=1):
	obs = env.reset()
	# env.render()
	num_epi = 0
	total_r = 0
	from tqdm import tqdm
	for i in tqdm(range(0, num_trials)):

		done = False
		# input("Enter")
		while not done:
			action = env.action_space.sample()
			obs, reward, done, info = env.step(action)
			# env.render()
			total_r += reward
			if done:
				obs = env.reset()
				num_epi += 1

	return total_r / num_epi