class GameDS:
	def __init__(self, my_players=None, op_players=None, ball=None, game_state=None):
		self.my_players = my_players
		self.op_players = op_players
		self.game_state = game_state
		self.ball = ball

	def get_num_my_players(self):
		return len(self.my_players)

	def get_num_op_players(self):
		return len(self.op_players)

	def initialize_ctrl_idx_map(self, ctrl_idx_to_player, player_to_ctrl_idx):
		self.ctrl_idx_to_player = ctrl_idx_to_player
		self.player_to_ctrl_idx = player_to_ctrl_idx