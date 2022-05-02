import numpy as np
from regex import E 
import tensorflow as tf
import time
from tensorflow.python.ops import init_ops
from tensorflow.python.training.moving_averages import assign_moving_average
from torch import float32



def neural_net(x, neurons, is_training, name, mv_decay = 0.9, dtype = tf.float32):

    def batch_normali(_x): 
        beta = tf.compat.v1.get_variable('beta', [_x.get_shape()[-1]], dtype, init_ops.zeros_initializer() )
        gamma = tf.compat.v1.get_variable('gamma', [_x.get_shape()[-1]], dtype, init_ops.ones_initializer() )
        mv_mean = tf.compat.v1.get_variable('mv_mean', [_x.get_shape()[-1]], dtype, init_ops.zeros_initializer(), trainable=False)
        mv_variance = tf.compat.v1.get_variable('mv_variance', [_x.get_shape()[-1]], dtype, init_ops.ones_initializer(), trainable=False)

        mean, variance = tf.nn.moments(x=_x, axes=[0], name='moments')
        tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.UPDATE_OPS, assign_moving_average(mv_mean,mean,mv_decay, True))
        tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.UPDATE_OPS, assign_moving_average(mv_variance, variance, mv_decay, False))

        mean, variance = tf.cond(pred=is_training, true_fn = lambda: (mean,variance), false_fn=lambda: (mv_mean, mv_variance))
        return tf.nn.batch_normalization(_x, mean, variance, beta, gamma, 1e-6)

    def layer(_x, out_size, activation_fn): 
        w = tf.compat.v1.get_variable('weights',[_x.get_shape().as_list()[-1], out_size], dtype, tf.keras.initializers.GlorotNormal())
        return activation_fn(batch_normali(tf.matmul(_x,w)))

    with tf.compat.v1.variable_scope(name): 
        x = batch_normali(x)
        for i in range(len(neurons)): 
            with tf.compat.v1.variable_scope('Layer_%i_' & (i+1)): 
                x = layer(x, neurons[i], tf.nn.tanh if i < len(neurons) -1 else tf.identity)
    
    return x 



def kolmogorov_train_test(xi, s_sde, phi, u_reference, neurons, lr_boundaries, lr_values, train_steps, mc_rounds, mc_freq, file_name, dtype=float32): 

    def approx_erros(): 
        lr, gs = sess.run ([learning_rate, global_step])
        