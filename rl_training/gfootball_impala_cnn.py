from typing import Tuple
import gym
from stable_baselines3.common.preprocessing import is_image_space
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from torch import nn
import torch as th


class GfootballImpalaCNN(BaseFeaturesExtractor):
    """
    gfootball_impala_cnn is architecture used in the paper
    (https://arxiv.org/pdf/1907.11180.pdf).
    It is illustrated in the appendix. It is similar to Large architecture
    from IMPALA paper; we use 4 big blocks instead of 3 though.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        super(GfootballImpalaCNN, self).__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        assert is_image_space(observation_space), (
            "You should use CNN only with images"
        )
        assert features_dim==256, "To replicate the same network"
        n_input_channels = observation_space.shape[0]

        self.conv_layers_config = [(16, 2), (32, 2), (32, 2), (32, 2)]
        self.pool = nn.MaxPool2d(kernel_size=3, stride=2)


        self.conv_blocks = [
            nn.Conv2d(in_channels=n_input_channels, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1)
        ]

        #https://www.tensorflow.org/api_docs/python/tf/nn/pool  -> If padding = "SAME": output_spatial_shape[i] = ceil(input_spatial_shape[i] / strides[i])
        self.pools = [nn.MaxPool2d(kernel_size=3, stride=2, padding=1) for _ in range(4)]

        self.resblocks_1 = [
            self.create_basic_res_block(16, 16),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32)
        ]
        self.resblocks_2 = [
            self.create_basic_res_block(16, 16),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32),
            self.create_basic_res_block(32, 32)
        ]

        self.relu = nn.ReLU()
        self.flatten = nn.Flatten()


        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.feat_extract(
                th.as_tensor(observation_space.sample()[None]).float()
            )
            n_flatten = n_flatten.shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU()) #n_flatten=960


    def create_basic_res_block(self, in_channel, out_channel):
        return nn.Sequential(
            nn.ReLU(),
            nn.Conv2d(in_channels=in_channel, out_channels=out_channel, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=out_channel, out_channels=out_channel, kernel_size=3, stride=1, padding=1),
        )

    def feat_extract(self, observations: th.Tensor) -> th.Tensor:
        observations = observations.float()
        observations /= 255

        conv_out = observations
        for i in range(4):
            conv_out = self.conv_blocks[i](conv_out)
            conv_out = self.pools[i](conv_out)

            block_input = conv_out
            conv_out = self.resblocks_1[i](conv_out)
            conv_out += block_input

            block_input = conv_out
            conv_out = self.resblocks_2[i](conv_out)
            conv_out += block_input

        conv_out = self.relu(conv_out)
        conv_out = self.flatten(conv_out)
        return conv_out

    def forward(self, observations: th.Tensor) -> th.Tensor:
        conv_out = self.feat_extract(observations)
        conv_out = self.linear(conv_out)

        return conv_out