from . import *
def build_scenario(builder):
	builder.config().game_duration = 25
	builder.config().deterministic = False
	builder.config().offsides = False
	builder.config().end_episode_on_score = True
	builder.config().end_episode_on_out_of_play = True
	builder.config().end_episode_on_possession_change = True

	builder.SetBallPosition(0.1, -0.1)

	builder.SetTeam(Team.e_Left)
	builder.AddPlayer(-0.98, -0.0, e_PlayerRole_GK)
	builder.AddPlayer(0.8608369104545457, 0.18710961165089016, e_PlayerRole_AM)
	builder.AddPlayer(0.9152431910064014, -0.1738734450923094, e_PlayerRole_CF)
	builder.AddPlayer(0.8947427764417378, -0.02552023211420238, e_PlayerRole_CM)


	builder.SetTeam(Team.e_Right)
	builder.AddPlayer(-0.98, 0.0, e_PlayerRole_GK)
	builder.AddPlayer(-0.75, 0.1, e_PlayerRole_CB)


