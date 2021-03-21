from . import *

DEBUG = False 
dump_file = "scene_data_log"
if DEBUG:
  import os 
  #print("os.getcwd", os.getcwd()) 
  print("Scene data is dumped in : ",  os.getcwd(), dump_file)


def build_scenario(builder):
    import pickle

    scene_info = pickle.load(open(data_path, "rb"))

    dump_str = ""
    if DEBUG:
      dump_str += "\n\nin gf scenario file, new scene\n"
      dump_str += f"Ball: {scene_info.ball}\n"

    for param, value in scene_info.params.items():
        #print(f"setting {param} to {value}")
        setattr(builder.config(), param, value)


    builder.SetBallPosition(scene_info.ball[0], scene_info.ball[1])

    builder.SetTeam(Team.e_Left)
    for mp in scene_info.my_players:
      #print(mp[0], mp[1], mp[2])
      builder.AddPlayer(mp[0], mp[1], mp[2])

      if DEBUG:
        dump_str += f"My Player: {mp[0]}, {mp[1]}, {mp[2]}\n"

    if len(scene_info.op_players)>0:
        builder.SetTeam(Team.e_Right)
        for op in scene_info.op_players:
          builder.AddPlayer(op[0], op[1], op[2])
          if DEBUG:
            dump_str += f"Op Player: {op[0]}, {op[1]}, {op[2]}\n"


    if DEBUG: 
      with open(dump_file, "a+") as f:
        f.write(dump_str)
        f.flush()
        