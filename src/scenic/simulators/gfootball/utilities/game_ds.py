import math
import numpy as np

class GameDS:
	def __init__(self, my_players=None, op_players=None, ball=None, game_state=None, scene=None):
		self.my_players = my_players
		self.op_players = op_players

		self.left_players = my_players
		self.right_players = op_players

		self.game_state = game_state
		self.ball = ball
		self.scene = scene

	def get_num_my_players(self):
		return len(self.my_players)

	def get_num_op_players(self):
		return len(self.op_players)

	def initialize_player_idx_map(self, left_idx_to_player, left_player_to_idx, right_idx_to_player, right_player_to_idx):
		self.left_idx_to_player = left_idx_to_player
		self.left_player_to_idx = left_player_to_idx
		self.right_idx_to_player = right_idx_to_player
		self.right_player_to_idx = right_player_to_idx

	def initialize_ctrl_idx_map(self, ctrl_idx_to_player, player_to_ctrl_idx):
		self.ctrl_idx_to_player = ctrl_idx_to_player
		self.player_to_ctrl_idx = player_to_ctrl_idx

	def is_manual_controlled(self):
		return self.scene.params["manual_control"]

	def get_num_controlled(self):
		if self.is_manual_controlled():
			return self.get_num_my_players()
		else:
			return self.get_num_my_players()+self.get_num_op_players()

	def get_designated_player_idx(self):
		'''
		This returns a list of designated players' indexes
		'''
		if isinstance(self.designated_player_idx, list):
			return self.designated_player_idx
		return [self.designated_player_idx]


	def compute_designated_from_obs(self):
		pass

	def compute_designated_as_closest_idx(self, num_player=1):
		df = lambda p1,p2: np.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

		dists = {p: df(p.position, self.ball.position) for p in self.my_players}

		if num_player > 1:
			# multiagent dynamic mode
			players = sorted(dists, key=dists.get)[:num_player]
			self.designated_player = players
			self.designated_player_idx = [self.player_to_ctrl_idx[player] for player in players]
			return self.designated_player_idx

		else:
			player = min(dists, key=dists.get)
			#print("player in control: ", player)
			self.designated_player = player
			self.designated_player_idx = self.player_to_ctrl_idx[player]
			return [self.designated_player_idx]

	def compute_designated_as_fixed(self, include_GK: bool):
		# notice we should have at least 2 left players including GK
		if not include_GK:
			players = [p for p in self.my_players if "GK" not in p.role]
			assert len(players) == (len(self.my_players) - 1), "Could not exclude GK."
		else:
			players = self.my_players

		# # use this to print the order of controlled players
		# print([self.player_str_mini(p) for p in players])

		self.designated_player = players
		self.designated_player_idx = [self.player_to_ctrl_idx[player] for player in players]
		return self.designated_player_idx



	@staticmethod
	def player_str(player):
		import math
		prev_pos = ""
		if hasattr(player, "prev_pos"):
			prev_pos = "   Prev Pos: ({player.position_prev.x:0.2f}, {player.position_prev.y:0.2f}) "
		return (f"{player.role}   P: ({player.position.x:0.2f}, {player.position.y:0.2f})   D: {math.degrees(player.direction):0.2f}"
			  f"   H: {math.degrees(player.heading):0.2f}   V: ({player.velocity.x:0.2f}, {player.velocity.y:0.2f})"
			  f"   Own: {player.owns_ball}{prev_pos}")

	@staticmethod
	def player_str_mini(player):
		#return f"{player.role}  ({player.position.x:0.2f}, {player.position.y:0.2f})"
		return f"{player.role}  ({player.position.x:0.2f}, {player.position.y:0.2f}) Controlled: {player.is_controlled} Owns: {player.owns_ball}"

	@staticmethod
	def ball_str_mini(ball):

		return f"({ball.position.x:0.2f}, {ball.position.y:0.2f})"

	@staticmethod
	def ball_str(ball):

		return (f"P: ({ball.position.x:0.2f}, {ball.position.y:0.2f})   D: {math.degrees(ball.direction):0.2f}"
			  f"   H: {math.degrees(ball.heading):0.2f}   V: ({ball.velocity.x:0.2f}, {ball.velocity.y:0.2f})")

	def print_ds(self):
		print("My Players")
		for mp in self.my_players:
			print(self.player_str(mp))

		print()
		print("Op Players")
		for op in self.op_players:
			print(self.player_str(op))

		print("ball")
		print(self.ball_str(self.ball))

		print()
		print()

	def print_mini(self):

		print("Ball: ", self.ball_str_mini(self.ball))
		print()

		print(f"My Team ({len(self.my_players)})")
		for mp in self.my_players:
			print(self.player_str_mini(mp))

		print()
		print(f"Op Team({len(self.op_players)})")
		for op in self.op_players:
			print(self.player_str_mini(op))



		print()
		print()