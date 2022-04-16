def get_num_left_controlled(player_control_mode, internal_control_left):
	'''
	A helper function that determines the value of num_left_controlled
	and num_left_dynamically_controlled to be used in the simulator.
	internal_control_left is the total number of left players in the scene.
	Warning: simulator needs to set both number to function correctly.
	'''
	# this is the number of left players that is dynamically controlled, if fixed control this is 0
	num_left_dynamically_controlled = 0
	# this is the number of left players controlled in total
	num_left_controlled = 1

	player_control_mode = str(player_control_mode)
	if player_control_mode == "all":
		num_left_controlled = internal_control_left

	elif player_control_mode == "allNonGK":
		assert internal_control_left > 1, "Scenario must have at least 2 left players."
		num_left_controlled = internal_control_left - 1

	elif player_control_mode.isnumeric():
		num_left_controlled = int(player_control_mode)
		if not (1 < num_left_controlled <= internal_control_left):
			raise ValueError(
				f"player_control_mode must be a valid integer if controlled players are fixed. Got: {num_left_controlled}")

	elif player_control_mode == "1closest":
		# this is single agent control, choose the closest
		num_left_dynamically_controlled = 1
		num_left_controlled = 1

	elif player_control_mode == "2closest":
		num_left_dynamically_controlled = 2
		num_left_controlled = 2
		if not (num_left_dynamically_controlled <= internal_control_left):
			raise ValueError(
				f"Number of player greater than total number of left players. Got: {num_left_dynamically_controlled}")

	elif player_control_mode == "3closest":
		num_left_dynamically_controlled = 3
		num_left_controlled = 3
		if not (num_left_dynamically_controlled <= internal_control_left):
			raise ValueError(
				f"Number of player greater than total number of left players. Got: {num_left_dynamically_controlled}")

	else:
		raise ValueError(
			f'player_control_mode must be "1closest" or "2closest" or "3closest" for dynamic control. Or be a number > 1, or "all", or "allNonGK" for fixed control mode. Got: {player_control_mode}')

	return num_left_controlled, num_left_dynamically_controlled






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