from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import tensorflow as tf

class TensorboardCallback(BaseCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """
    def __init__(self, verbose=0):
        self.is_tb_set = False
        super(TensorboardCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # Log additional tensor
        """
        if not self.is_tb_set:

            with self.model.graph.as_default():
                tf.summary.scalar('value_target', tf.reduce_mean(self.model.value_target))
                self.model.summary = tf.summary.merge_all()
            self.is_tb_set = True

            # Log scalar value (here a random variable)
            value = np.random.random()
            summary = tf.Summary(value=[tf.Summary.Value(tag='random_value', simple_value=value)])
            self.locals['writer'].add_summary(summary, self.num_timesteps)
        """
        pass