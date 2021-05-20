import numpy as np
class GFDset(object):
    
    def __init__(self, inputs, labels, info, randomize=True):
        
        #traj_data = np.load(expert_path)
        
        self.inputs = inputs
        self.obs  = self.inputs
        self.labels = labels
        self.acts = self.labels
        self.info = info
        for k,v in info.items():
            if k in ["obs", "acs"]: continue 
            setattr(self, k, v)
            

        assert len(self.inputs) == len(self.labels)
        self.randomize = randomize
        self.num_pairs = self.inputs.shape[0]
        self.size = self.num_pairs 
        self.init_pointer()

    def init_pointer(self):
        self.pointer = 0
        if self.randomize:
            idx = np.arange(self.num_pairs)
            np.random.shuffle(idx)
            self.inputs = self.inputs[idx, :]
            self.labels = self.labels[idx, :]

    def get_next_batch(self, batch_size):
        # if batch_size is negative -> return all
        if batch_size < 0:
            return self.inputs, self.labels
        if self.pointer + batch_size >= self.num_pairs:
            self.init_pointer()
        end = self.pointer + batch_size
        inputs = self.inputs[self.pointer:end, :]
        labels = self.labels[self.pointer:end, :]
        self.pointer = end
        return inputs, labels

    def summary(self):
        msg = ""

        msg += f"Obs Shape: {self.obs.shape}\n"
        msg += f"Act Shape: {self.acts.shape}\n"

        for k, v in self.info.items():
            if k in ["rewards"]:continue
            msg += f"{k}: {v}\n"

        return msg


def get_datasets(path, validation_ratio=0.2):
    traj_data = np.load(path)

    inputs = traj_data["obs"]
    labels = traj_data["acs"]
    
    info = {}
    for k,v in traj_data.items():
        if k in ["obs", "acs"]: continue 
        info[k] = v 
    

    assert len(inputs) == len(labels)

    
    n = inputs.shape[0]

    #val_n = int(n*validation_ratio)
    train_n = n-int(n*validation_ratio)

    idx = np.arange(n)
    np.random.shuffle(idx)

    t_idx = idx[0:train_n]
    v_idx = idx[train_n:]

    train_inputs = inputs[t_idx, :]
    train_labels = labels[t_idx, :]

    val_inputs = inputs[v_idx, :]
    val_labels = labels[v_idx, :]

    tds = GFDset(train_inputs, train_labels, info)
    vds = GFDset(val_inputs, val_labels, info)

    return tds, vds
    
    #self.inputs = self.inputs[idx, :]
    #self.labels = self.labels[idx, :]

 

if __name__ == "__main__":

    path = "/home/ubuntu/ScenicGFootBall/training/gfrl/_data/sc4rl_fg11v1_rns_success_10000.npz"
    #path = "/home/ubuntu/ScenicGFootBall/training/gfrl/_data/pns_1000.npz"

    tds, vds = get_datasets(path, validation_ratio=0.0)

    print("train")
    print(tds.summary())
    print()

    print("validation")
    print(vds.summary())
    print()


    
