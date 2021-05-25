from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


# -----Behavior-----
behavior P1Behavior():
    target_player = p2
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
        safe_players = [p for p in simulation().game_ds.my_players if p not in danger_cone]
        # safe_players = simulation().game_ds.my_players
        selected_p = get_closest_player_info(self.position, safe_players)[0]
        # print(get_direction(*self.position, *selected_p.position))
        do ShortPassTo(selected_p)


behavior CloseInAndShoot():
    ds = simulation().game_ds
    destination_point = Point at 99 @ 0

    try:
        do MoveToPosition(destination_point, sprint=False)
    interrupt when opponentInRunway(self, reactionDistance=8):
        # do dribble_evasive_zigzag(destination_point)
        # print("danger. Pass.")
        do SafePass(20, 0.5)
        # take Pass()
    interrupt when blue_penaltyBox.containsPoint(self.position):
        # take ReleaseDirection()
        do AimGoalCornerAndShoot()

    do IdleBehavior()


# -----SET UP-----
ball = Ball at 26 @ 11

# Left Team
ego = YellowGK at -99 @ 0, with behavior IdleBehavior()
YellowLB at -67.2 @ 19.576, with behavior CloseInAndShoot()
YellowCB at -75 @ 6.356, with behavior CloseInAndShoot()
YellowCB at -75 @ -6.3559, with behavior CloseInAndShoot()
YellowRB at -67.2 @ -19.576, with behavior CloseInAndShoot()
YellowCM at -43.4 @ 10.568, with behavior CloseInAndShoot()
YellowCM at -43.4 @ -10.568, with behavior CloseInAndShoot()
p4 = YellowCM at 50 @ 31.61, with behavior CloseInAndShoot()
# Player with ball at the beginning
p1 = YellowLM at 25 @ 10, with behavior P1Behavior()
# good candidate down
p2 = YellowRM at 25 @ -10, with behavior CloseInAndShoot()
# good candidate top
p3 = YellowCF at 35 @ -31.61, with behavior CloseInAndShoot()


# Right Team
opgk = BlueGK at 99 @ 0
BlueLB at -12.8 @ -19.576
BlueCB at -40 @ -6.356
BlueCB at 40 @ 6.3559
BlueRB at -12.8 @ -19.576
BlueCM at -36.5 @ -10.568
BlueCM at -28.2 @ 0
BlueCM at -36.5 @ 10.568
BlueLM at -54 @ -31.61
BlueRM at -51 @ 0
BlueCF at -54 @ 31.6102


