from . import *


def build_scenario(builder):
    import pickle

    scene_info = pickle.load(open(data_path, "rb"))

    #print(f"in gf scenario")
    #print(scene_info.ball)

    for param, value in scene_info.params.items():
        #print(f"setting {param} to {value}")
        setattr(builder.config(), param, value)


    builder.SetBallPosition(scene_info.ball[0], scene_info.ball[1])

    builder.SetTeam(Team.e_Left)
    for mp in scene_info.my_players:
      #print(mp[0], mp[1], mp[2])
      builder.AddPlayer(mp[0], mp[1], mp[2])

    if len(scene_info.op_players)>0:
        builder.SetTeam(Team.e_Right)
        for op in scene_info.op_players:
          builder.AddPlayer(op[0], op[1], op[2])