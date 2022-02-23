import numpy as np
from typing import Dict, List
import gym

from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.torch.misc import (
    normc_initializer,
    same_padding,
    SlimConv2d,
    SlimFC,
)
from ray.rllib.models.utils import get_activation_fn, get_filter_config
from ray.rllib.utils.annotations import override
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils.typing import ModelConfigDict, TensorType

torch, nn = try_import_torch()


# the convolution layer of deepmind
class DeepMind(nn.Module):
    def __init__(self):
        super(DeepMind, self).__init__()
        self.conv1 = nn.Conv2d(16, 32, 8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
        self.conv3 = nn.Conv2d(64, 32, 3, stride=1)
        self.fc1 = nn.Linear(32 * 5 * 8, 512)
        # start to do the init...
        nn.init.orthogonal_(self.conv1.weight.data, gain=nn.init.calculate_gain('relu'))
        nn.init.orthogonal_(self.conv2.weight.data, gain=nn.init.calculate_gain('relu'))
        nn.init.orthogonal_(self.conv3.weight.data, gain=nn.init.calculate_gain('relu'))
        nn.init.orthogonal_(self.fc1.weight.data, gain=nn.init.calculate_gain('relu'))
        # init the bias...
        nn.init.constant_(self.conv1.bias.data, 0)
        nn.init.constant_(self.conv2.bias.data, 0)
        nn.init.constant_(self.conv3.bias.data, 0)
        nn.init.constant_(self.fc1.bias.data, 0)

    def forward(self, x):
        assert x.shape[1] == 16 and x.shape[2] == 72 and x.shape[3] == 96, f"Wrong input obs shape {x.shape}"
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.relu(self.conv3(x))
        # print(x.shape)  # torch.Size([16, 32, 5, 8])
        # if x.shape[0] != 16:
        #     print(x.shape)

        x = x.reshape((-1, 32 * 5 * 8))
        x = nn.functional.relu(self.fc1(x))

        return x


class NatureCNN(TorchModelV2, nn.Module):
    """Nature CNN network."""

    def __init__(
        self,
        obs_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        num_outputs: int,
        model_config: ModelConfigDict,
        name: str,
    ):
        TorchModelV2.__init__(
            self, obs_space, action_space, num_outputs, model_config, name
        )
        nn.Module.__init__(self)

        (w, h, in_channels) = obs_space.shape

        self._convs = DeepMind()

        # If our num_outputs still unknown, we need to do a test pass to
        # figure out the output dimensions. This could be the case, if we have
        # the Flatten layer at the end.
        if self.num_outputs is None:
            # Create a B=1 dummy sample and push it through out conv-net.
            dummy_in = (
                torch.from_numpy(self.obs_space.sample())
                .permute(2, 0, 1)
                .unsqueeze(0)
                .float()
            )
            dummy_out = self._convs(dummy_in)
            self.num_outputs = dummy_out.shape[1]
        print(f"num_outputs={self.num_outputs}")

        # Build the value layers
        self._value_branch = nn.Linear(512, 1)
        self._logits = nn.Linear(512, action_space.n)

        # init the value layer..
        nn.init.orthogonal_(self._value_branch.weight.data)
        nn.init.constant_(self._value_branch.bias.data, 0)
        # init the actor layer...
        nn.init.orthogonal_(self._logits.weight.data, gain=0.01)
        nn.init.constant_(self._logits.bias.data, 0)

        # Holds the current "base" output (before logits layer).
        self._features = None

    @override(TorchModelV2)
    def forward(
        self,
        input_dict: Dict[str, TensorType],
        state: List[TensorType],
        seq_lens: TensorType,
    ) -> (TensorType, List[TensorType]):

        self._features = input_dict["obs"].float() / 255
        # Permuate b/c data comes in as [B, dim, dim, channels]:
        self._features = self._features.permute(0, 3, 1, 2)

        conv_out = self._convs(self._features)
        # Store features to save forward pass when getting value_function out.
        self._features = conv_out
        logits = self._logits(conv_out)

        return logits, state

    @override(TorchModelV2)
    def value_function(self) -> TensorType:
        assert self._features is not None, "must call forward() first"

        features = self._features
        return self._value_branch(features).squeeze(1)

    # def _hidden_layers(self, obs: TensorType) -> TensorType:
    #     res = self._convs(obs.permute(0, 3, 1, 2))  # switch to channel-major
    #     res = res.squeeze(3)
    #     res = res.squeeze(2)
    #     return res

