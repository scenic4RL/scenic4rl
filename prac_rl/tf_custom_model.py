from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.registry import register_env
from ray import tune
import sonnet as snt

import gym, ray
from ray.rllib.agents import ppo
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

import argparse
import os

import ray
from ray import tune
from ray.rllib.agents.dqn.distributional_q_tf_model import \
    DistributionalQTFModel
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.misc import normc_initializer
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.visionnet import VisionNetwork as MyVisionNetwork
from ray.rllib.policy.policy import LEARNER_STATS_KEY
from ray.rllib.policy.sample_batch import DEFAULT_POLICY_ID
from ray.rllib.utils.framework import try_import_tf

tf1, tf, tfv = try_import_tf()


def env_creator(env_config):

    gf_env_settings = {
                "stacked": True,
                "rewards": 'scoring,checkpoints',
                "representation": 'extracted',
                "players": [f"agent:left_players=1"],
                "real_time": False,
                "action_set": "default"
            }

    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    scenario_file = f"academy_empty_goal_close.scenic"
    scenario = buildScenario(scenario_file)
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
    print("env instance created")
    return env 

ray.init()


class MyKerasModel(TFModelV2):
    """Custom model for policy gradient algorithms."""

    def __init__(self, obs_space, action_space, num_outputs, model_config,
                 name):
        super(MyKerasModel, self).__init__(obs_space, action_space,
                                           num_outputs, model_config, name)

        self.inputs = tf.keras.layers.Input(
            shape=obs_space.shape, name="observations")


        self.conv1 = tf.keras.layers.Conv2D(
            filters=16,
            kernel_size=3, 
            padding="same",
            input_shape=""
        )

        self.conv2 = tf.keras.layers.Conv2D(
            filters=32,
            kernel_size=3
        )

        self.linear = tf.keras.layers.Dense(units=256)


        """
        layer_1 = tf.keras.layers.Dense(
            128,
            name="my_layer1",
            activation=tf.nn.relu,
            kernel_initializer=normc_initializer(1.0))(self.inputs)
        layer_out = tf.keras.layers.Dense(
            num_outputs,
            name="my_out",
            activation=None,
            kernel_initializer=normc_initializer(0.01))(layer_1)
        value_out = tf.keras.layers.Dense(
            1,
            name="value_out",
            activation=None,
            kernel_initializer=normc_initializer(0.01))(layer_1)

        """
        
        #self.base_model = tf.keras.Model(self.inputs, [layer_out, value_out])

    def forward(self, input_dict, state, seq_lens):
        print("ZZZZ", input_dict["obs"]) #Tensor("default_policy/obs:0", shape=(?, 72, 96, 16), dtype=uint8)
        print("ZZZZ", input_dict["obs"].shape) #(?, 72, 96, 16)
        
        frame = input_dict["obs"]
        frame = tf.to_float(frame)
        frame /= 255

        print("obs", frame)

        conv_out =  self.conv1(frame)
        print("conv out 1", conv_out)

        conv_out = tf.nn.pool(
            conv_out,
            window_shape=[3, 3],
            pooling_type='MAX',
            padding='SAME',
            strides=[2, 2])

        print("pool out 1", conv_out) 
    
        conv_out = tf.nn.relu(conv_out)
        conv_out = tf.keras.layers.Flatten()(conv_out)
        print("flatten", conv_out) 

        out = self.linear(conv_out)
        print("linear", out)

        model_out, self._value_out = self.base_model(input_dict["obs"])
        return model_out, state

    def value_function(self):
        return tf.reshape(self._value_out, [-1])

    def metrics(self):
        return {"foo": tf.constant(42.0)}




register_env("my_env", env_creator)
ModelCatalog.register_custom_model("gf_impala_cnn_ppo_keras", MyKerasModel)


from ray.rllib.agents.ppo import PPOTrainer
tune.run(PPOTrainer, config={
    "env": "my_env", 
    "num_workers": 2,
    'model': {
        "custom_model": "gf_impala_cnn_ppo_keras"
        },

}) 


"""
    'model': {
                    'dim':96,
                'conv_filters': [
                    [96,16,96]
                ],
                'fcnet_hiddens': [256, 256],
                'use_lstm': False,
            }
"""

