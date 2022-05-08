from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


# -----Behavior-----
behavior ShortPassTo(player):
    '''
    Always try to pass. If not owned ball, will move to the ball.
    '''
    is_player_rightTeam = self.team == "right"
    #take MoveTowardsPoint(player.position, self.position, is_player_rightTeam)
    take Pass("short")
    take ReleaseSprint()
    take ReleaseDirection()

behavior P1Behavior():
    # target_player = p2
    ds = simulation().game_ds
    target_player = None
    for p in ds.left_players:
        if p.role == "RM":
            target_player = p

    # make sure we turn
    take SetDirection(6)
    take SetDirection(6)
    take SetDirection(6)
    take SetDirection(6)
    do ShortPassTo(target_player)
    do CloseInAndShoot()

behavior SafePass(danger_cone_radius, danger_cone_angle):
    if not self.owns_ball:
        take ReleaseDirection()

    else:
        danger_cone = SectorRegion(self, danger_cone_radius, self.heading, danger_cone_angle)
        safe_players = [p for p in simulation().game_ds.left_players if p not in danger_cone]
        # safe_players = simulation().game_ds.my_players
        selected_p = get_closest_player_info(self, safe_players)[0]
        # selected_p = get_closest_player_info(right_goal_midpoint, safe_players)[0]

        do ShortPassTo(selected_p)


behavior CloseInAndShoot():
    ds = simulation().game_ds
    destination_point = Point at 99 @ 0

    try:
        do MoveToPosition(destination_point, sprint=True)

    interrupt when opponentInRunway(self, reactionDistance=8):
        # do dribble_evasive_zigzag(destination_point)
        # print("danger. Pass.")
        do SafePass(20, 0.5)
        # take Pass()
    interrupt when right_penaltyBox.containsPoint(self.position):
        # take ReleaseDirection()
        do AimGoalCornerAndShoot()

    do IdleBehavior()


# -----SET UP-----
ball = Ball at 26 @ 11

# Left Team
ego = LeftGK at -99 @ 0
LeftLB at -67.2 @ 19.576
LeftCB at -75 @ 6.356
LeftCB at -75 @ -6.3559
LeftRB at -67.2 @ -19.576
LeftCM at -43.4 @ 10.568
LeftCM at -43.4 @ -10.568

# one of the three controlled players
p4 = LeftCM at 50 @ 31.61, with behavior CloseInAndShoot()
# Player with ball at the beginning
p1 = LeftLM at 25 @ 10, with behavior P1Behavior()
# good candidate down
p2 = LeftRM at 25 @ -10, with behavior CloseInAndShoot()
# good candidate top, not controlled
p3 = LeftCF at 35 @ -31.61


# Right Team
opgk = RightGK at 99 @ 0
RightLB at -12 @ -19
RightCB at -40 @ -6.356
RightCB at 40 @ 6.3559
RightRB at -13.5 @ -20.5
RightCM at -36.5 @ -10.568
RightCM at -28.2 @ 0
RightCM at -36.5 @ 10.568
RightLM at -54 @ -31.61
RightRM at -51 @ 0
RightCF at -54 @ 31.6102


