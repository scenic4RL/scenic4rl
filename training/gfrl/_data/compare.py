import numpy as np

file_path_1 = "/Users/markwu/Works/football/ScenicGFootBall/training/gfrl/_data/compare_envv2_new_counterattack_easy.npz"
file_path_2 = "/Users/markwu/Works/football/ScenicGFootBall/training/gfrl/_data/compare_py37_counterattack_easy.npz"

traj_data_1 = np.load(file_path_1)
inputs_1 = traj_data_1["obs"]
labels_1 = traj_data_1["acs"]

traj_data_2 = np.load(file_path_2)
inputs_2 = traj_data_2["obs"]
labels_2 = traj_data_2["acs"]

print(labels_1.shape)
print(labels_2.shape)

for i in range(100):
    if not np.array_equal(inputs_1[i], inputs_2[i]):
        print("Mismatch at ", i)
        # break
    else:
        if True or not np.array_equal(labels_1[i], labels_2[i]):
            print(i, np.nonzero(labels_1[i]), np.nonzero(labels_2[i]))