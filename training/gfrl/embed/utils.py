from collections import namedtuple
Trajectory = namedtuple('Trajectory', ["obs_arr", "gt_arr", "act_arr", "rew_arr", "info_arr"])
