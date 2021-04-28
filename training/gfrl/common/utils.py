def get_incremental_dirname(path, dirname):
    import os
    
    name =  lambda path, dirname, x: f"{os.path.join(path, dirname)}_{x}"
    i = 0
    while os.path.exists(name(path, dirname, i)):
        #print(f"/{path}/{dirname}_{i}")
        i += 1

    os.makedirs(name(path, dirname, i), exist_ok=True)
    return name(path, dirname, i)


def save_params(dirpath, FLAGS):
    #print(dir(FLAGS))

    params = FLAGS.flag_values_dict()

    import os
    os.makedirs(dirpath, exist_ok=True)
    param_filename = os.path.join(dirpath+"/params.txt")
    with open(param_filename, "w+") as ff:
        from pprint import pprint
        pprint(params, stream=ff)

    import pickle
    param_filename = os.path.join(dirpath + "/params.p")
    with open(param_filename, "wb") as ff:
        pickle.dump(params, ff)


