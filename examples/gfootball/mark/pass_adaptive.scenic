from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False

# ----- Constants -----
init_triangle_length = 35

danger_cone_angle = 70 deg
danger_cone_radius = 20

pass_distance = 10

# ----- Behaviors -----
def player_with_ball(ds, ball):
    if (ball.owned_team == 0):
        return ds.my_players[ball.owned_player_idx]
    # if (ball.owned_team == 1):
    #     return ds.op_players[ball.owned_player_idx]
    return None

def get_closest_player(position, players):
    min_distance = None
    closest_player = None

    for p in players:
        dist = math.sqrt(math.pow(p.x - position[0], 2) + math.pow(p.y - position[1], 2))
        if dist == 0:
            continue
        if min_distance is None or dist < min_distance:
            closest_player = p
            min_distance = dist
    return closest_player, min_distance

'''
Try to keep an open position to receive ball
'''
behavior KeepPosition(center):
    ds = simulation().game_ds
    while True:
        p = player_with_ball(ds, ball)

        if p is not None and p != self:
            # check if opponent is in the way
            relative_heading = angle from p to self
            danger_cone = SectorRegion(p, danger_cone_radius, relative_heading, danger_cone_angle) # center, radius, heading, angle
            if any([op in danger_cone for op in ds.op_players]):
                #print("Ball in Danger!")
                # Now move out of the way. Move to closest cone edge
                h_a = -danger_cone_angle/2 relative to relative_heading
                h_b = danger_cone_angle/2 relative to relative_heading
                pt_a = Point at p offset along h_a by 0 @ danger_cone_radius
                pt_b = Point at p offset along h_b by 0 @ danger_cone_radius

                # TODO: check pt_a/b in bound
                target_pt = pt_a
                if (distance from self to pt_a) > (distance from self to pt_b):
                    target_pt = pt_b
                #print(target_pt.x,target_pt.y)
                # move to point
                do MoveToPosition(target_pt.x,target_pt.y)# for 1 seconds
                #print("Moved to target")
            else:
                #print("Ball not in danger.")
                # take NoAction()
                take MoveTowardsPoint(center.x, center.y, self.x, self.y)
        else:
            # if ball not owned by teammate
            # take NoAction()
            take MoveTowardsPoint(center.x, center.y, self.x, self.y)

'''
Try to pass to a teammate in safe position
'''
behavior SafePass():
    if not self.owns_ball:
        print("No Ball!!!")
    else:
        danger_cone = SectorRegion(self, danger_cone_radius, self.heading, danger_cone_angle)
        safe_players = [p for p in simulation().game_ds.my_players if p not in danger_cone]
        print("pass")
        do PassToPlayer(get_closest_player(self.position, safe_players)[0], "short")




'''
Try to keep an open position to receive ball
'''
behavior MoveAndPass(center):
    ds = simulation().game_ds
    try:
        do KeepPosition(center)
    interrupt when (self.owns_ball and get_closest_player(self.position, ds.op_players)[1] < pass_distance):
        #do PassToPlayer(get_closest_player(self.position, ds.my_players)[0], "short")
        do SafePass()



behavior OpponentBehavior(center):
    #do RunInCircle()
    #do BuiltinAIBot()
    # ball is a global variable
    try:
        do FollowObject(ball, opponent=True)
    interrupt when (distance from self to ball) < 6:
        print("reset")
        do MoveToPosition(center.x, center.y, opponent=True)
    interrupt when self.owns_ball:
        take Shoot()

# ----- Players -----

ego = MyGK# with behavior IdleBehavior()

p1_pos = Point on LeftReg_CM
# spawn p2 to top
p2_pos = Point at p1_pos offset along -30 deg by 0 @ init_triangle_length
# spawn p3 to right
p3_pos = Point at p1_pos offset along -90 deg by 0 @ init_triangle_length
# spawn enemy in between
o1_pos = Point at p1_pos offset along -60 deg by 0 @ init_triangle_length/1.42


# , facing toward right_goal_midpoint
p1 = MyPlayer with role "CM", at p1_pos, with behavior MoveAndPass(p1_pos)
p2 = MyPlayer with role "CM", at p2_pos, with behavior MoveAndPass(p2_pos)
p3 = MyPlayer with role "CM", at p3_pos, with behavior MoveAndPass(p3_pos)

o1 = OpPlayer with role "CM", at o1_pos, with behavior OpponentBehavior(o1_pos)
# o2 = OpCF
# o3 = OpCB
o0 = OpGK with behavior IdleBehavior()

#Ball
ball = Ball ahead of p1 by 2
