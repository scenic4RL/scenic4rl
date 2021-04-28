import numpy as np
class GFDset(object):
    
    def __init__(self, expert_path, randomize=True):
        
        traj_data = np.load(expert_path)
        
        self.inputs = traj_data["obs"]
        self.obs  = self.inputs
        self.labels = traj_data["acs"]
        self.acts = self.labels

        for k,v in traj_data.items():
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

