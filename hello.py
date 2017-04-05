import tensorflow as tf


def hello():
    hello = tf.constant("Hello, tensorflow!")
    sess = tf.Session()
    print(sess.run(hello))

if __name__ =="__main__":
    hello()
