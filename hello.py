import tensorflow as tf


def main(unused_argv):
    network = tf.constant("Hello, Tensorflow!")
    sess = tf.Session()
    print(sess.run(network))


if __name__ =="__main__":
    main([])


def __call__(self, *args, **kwargs):
    main([])
    return "Hello Complete!"
