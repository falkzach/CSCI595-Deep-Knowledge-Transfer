import tensorflow as tf


def main(unused_argv):
    network = tf.constant("Hello, Tensorflow!")
    sess = tf.Session()
    print(sess.run(network))
    return sess


if __name__ =="__main__":
    main([])


def __call__(self, *args, **kwargs):
    session = main([])
    return "Hello Complete!", session
