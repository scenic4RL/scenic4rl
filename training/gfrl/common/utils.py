def get_incremental_dirname(path, dirname):
    import os

    name =  lambda path, dirname, x: f"{os.path.join(path, dirname)}_{x}"
    i = 0
    while os.path.exists(name(path, dirname, i)):
        #print(f"/{path}/{dirname}_{i}")
        i += 1

    return name(path, dirname, i)
