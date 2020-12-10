from typing import List


class RoleCode:
    GK = 0
    CB = 1
    LB = 2
    RB = 3
    DM = 4
    CM = 5
    LM = 6
    RM = 7
    AM = 8
    CF = 9

    player_code_to_role = {
        0: "GK",
        1: "CB",
        2: "LB",
        3: "RB",
        4: "DM",
        5: "CM",
        6: "LM",
        7: "RM",
        8: "AM",
        9: "CF"
    }

    player_role_to_code = {
        "GK":0 ,
        "CB":1 ,
        "LB":2 ,
        "RB":3 ,
        "DM":4 ,
        "CM":5 ,
        "LM":6 ,
        "RM":7 ,
        "AM":8 ,
        "CF":9
    }

    @classmethod
    def code_to_role(cls, code:int):
        return cls.player_code_to_role[code]

    @classmethod
    def role_to_code(cls, code: int):
        return cls.player_role_to_code[code]




class ActionCode:




    """Default action set"""
    idle = 0

    """Movement Actions. All are sticky"""
    left = 1  # run to the left, sticky action.
    top_left = 2  # run to the top-left, sticky action.
    top = 3  # run to the top, sticky action.
    top_right = 4  # run to the top-right, sticky action.
    right = 5  # run to the right, sticky action.
    bottom_right = 6  # run to the bottom-right, sticky action.
    bottom = 7  # run to the bottom, sticky action.
    bottom_left = 8  # run to the bottom-left, sticky action.

    """Passing / Shooting: Direction based on movement/opponents goal"""
    long_pass = 9  # perform a long pass to the player on your team. Player to pass the ball to is auto-determined based on the movement direction.
    high_pass = 10  # similar to action_long_pass
    short_pass = 11  # similar to action_long_pass
    shot = 12  # perform a shot, always in the direction of the opponent's goal.

    """Other"""
    sprint = 13  # start sprinting, sticky
    release_direction = 14  # reset current movement direction.
    release_sprint = 15  # stop sprinting
    sliding = 16  # perform a slide (effective when not having a ball).
    dribble = 17  # start dribbling (effective when having a ball), sticky action. Player moves slower, but it is harder to take over the ball from him.
    release_dribble = 18  # stop dribbling

    """V2 action set"""
    builtin_ai = 19  # , let game's built-in AI generate an action

    sticky_actions = [left, top_left, top, top_right, right, bottom_right, bottom, bottom_left, sprint, dribble]
    #sticky_actions = [sprint, dribble, , right, top, bottom, top_left, top_right, bottom_left, bottom_right]
    act_id_to_act_map = {
        0: left,
        1: top_left,
        2:top, 3:top_right, 4:right, 5:bottom_right, 6:bottom, 7:bottom_left, 8:sprint, 9:dribble
    }

    @classmethod
    def sticky_direction(cls, s: List):

        for idx in range(len(s)):
            if s[idx]==1 and idx in cls.act_id_to_act_map:
                return cls.act_id_to_act_map[idx]

        return None
    @classmethod
    def is_sticky(cls, action:int):
        return action in cls.sticky_actions



    """Full Named Versions"""
    """Default action set"""
    action_idle = 0

    """Movement Actions. All are sticky"""
    action_left = 1                 #run to the left, sticky action.
    action_top_left = 2             #run to the top-left, sticky action.
    action_top = 3                  #run to the top, sticky action.
    action_top_right = 4            #run to the top-right, sticky action.
    action_right = 5                #run to the right, sticky action.
    action_bottom_right = 6         #run to the bottom-right, sticky action.
    action_bottom = 7               #run to the bottom, sticky action.
    action_bottom_left = 8          #run to the bottom-left, sticky action.

    """Passing / Shooting: Direction based on movement/opponents goal"""
    action_long_pass = 9            #perform a long pass to the player on your team. Player to pass the ball to is auto-determined based on the movement direction.
    action_high_pass = 10           #similar to action_long_pass
    action_short_pass = 11          #similar to action_long_pass
    action_shot = 12                #perform a shot, always in the direction of the opponent's goal.

    """Other"""
    action_sprint = 13              #start sprinting, sticky
    action_release_direction = 14   #reset current movement direction.
    action_release_sprint = 15      #stop sprinting
    action_sliding = 16             #perform a slide (effective when not having a ball).
    action_dribble = 17             #start dribbling (effective when having a ball), sticky action. Player moves slower, but it is harder to take over the ball from him.
    action_release_dribble = 18     #stop dribbling

    """V2 action set"""
    action_builtin_ai = 19          #, let game's built-in AI generate an action


