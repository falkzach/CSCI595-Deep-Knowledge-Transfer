#!/usr/bin/env python

import tensorflow as tf


def main(unused_argv):
    config = tf.ConfigProto(device_count={'GPU': 0})
    with tf.Session(config=config) as sess:

        node1 = tf.constant(3.0, tf.float32)
        node2 = tf.constant(4.0) # also tf.float32 implicitly

        node3 = tf.add(node1, node2)

        print("node1: ", node1)
        print("node2: ", node2)
        print("node3: ", node3)
        print("sess.run(node3): ", sess.run(node3))
    return sess

def __call__(self, *args, **kwargs):
    session = main([])
    return "Test 1 Complet!", session
