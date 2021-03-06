from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


# weight initializesrs

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

# convolution and pooling

def conv2d(x, W):
  return tf.nn.conv2d(
      x,
      W,
      strides=[1, 1, 1, 1],
      padding='SAME'
  )


def max_pool_2x2(x):
  return tf.nn.max_pool(
      x,
      ksize=[1, 2, 2, 1],
      strides=[1, 2, 2, 1],
      padding='SAME'
  )


if __name__  == "__main__":

    DEEP_LAYERS = 1024
    LEARNING_RATE = 1e-4 # 1e-3 for GD, 1e-4 for ADAM

    ###### SETUP ######

    # dataset, because we need data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

    # tensorflow interactive session, the connection to the C++ backend
    sess = tf.InteractiveSession()

    x = tf.placeholder(tf.float32, shape=[None, 784])   #input placeholder
    y_ = tf.placeholder(tf.float32, shape=[None, 10])   #output placeholder

    ###### SHAPE AND CONVULSE ON INPUT DATA TO REDUCE DIMENSIONALITY TO 7X7 ######

    # we must reshape the image (x) to a 4d tensor
    # QUESTION: what does the negative one represent??
    # second and third dimensions are image width x height
    # third dimension corresponds to number of channels (1, black (something) or white (nothing))
    x_image = tf.reshape(x, [-1, 28, 28, 1])

    # FIRST CONVULSION LAYER

    # convulse
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    # convolve the image
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    # max pool to a 14x14
    h_pool1 = max_pool_2x2(h_conv1)

    # SECOND CONVULSION LAYER

    # convulse
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    # pool
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    #for dropout and draining accuracy
    keep_prob = tf.placeholder(tf.float32) #only have one instance of this line

    ##
    ######DONT FIDDLE ABOVE HERE
    ##

    ###### HIDDEN LAYERS ######

    # Densely connected Layer 1
    W_fc1 = weight_variable([7 * 7 * 64, DEEP_LAYERS])
    b_fc1 = bias_variable([DEEP_LAYERS])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu6(tf.matmul(h_pool2_flat, W_fc1) + b_fc1) #our densly connected layer
    # h_fc16 = tf.nn.sigmoid(tf.matmul(h_pool2_flat, W_fc1) + b_fc1) #our densly connected layer

    ###### Interlayer DROPOUT ######
    # h_fc1_drop1 = tf.nn.dropout(h_fc1, keep_prob)

    ###### MORE HIDDEN LAYERS ######
    # W_fc12 = weight_variable([1024, 1024])
    # b_fc12 = bias_variable([1024])
    # h_fc12 = tf.nn.relu(tf.matmul(h_fc1, W_fc12) + b_fc12)  # our densly connected layer

    # DROPOUT
    # h_fc1_drop2 = tf.nn.dropout(h_fc12, keep_prob)

    ###### EVEN MORE ######
    # W_fc13 = weight_variable([1024, 1024])
    # b_fc13 = bias_variable([1024])
    # h_fc13 = tf.nn.relu(tf.matmul(h_fc1_drop2, W_fc13) + b_fc13)  # our densly connected layer

    # DROPOUT AGAIN
    # h_fc1_drop3 = tf.nn.dropout(h_fc13, keep_prob)

    # BATCH NORMALIZATION
    # epsilon = 1e-3      # Small epsilon value for the BN transform
    # scale = tf.Variable(tf.ones([1024]))
    # beta = tf.Variable(tf.zeros([1024]))
    # batch_mean, batch_var = tf.nn.moments(h_fc1, [0])
    # h_fcl_batch_norm = tf.nn.batch_normalization(h_fc1, batch_mean, batch_var, beta, scale, epsilon)

    ##
    ######DONT FIDDLE BELLOW HERE
    ##

    ###### READOUT AND VECTORIZE ######

    # READOUT LAYER
    W_fc2 = weight_variable([DEEP_LAYERS, 10])
    b_fc2 = bias_variable([10])

    # vectorize
    # vectorized image, times weights, plus bias
    ###
    ### Modify based out final layer
    ###
    y_conv = tf.matmul(h_fc1, W_fc2) + b_fc2        #Basic Single dense layer
    # y_conv = tf.matmul(h_fc1_drop1, W_fc2) + b_fc2     #With Dropout
    # y_conv = tf.matmul(h_fcl_batch_norm, W_fc2) + b_fc2     #With Batch Normalization
    # y_conv = tf.matmul(h_fc12, W_fc2) + b_fc2     #second strongly connected layer
    # y_conv = tf.matmul(h_fc1_drop3, W_fc2) + b_fc2     #third strongly connected layer
    # y_conv = tf.matmul(h_fc16, W_fc2) + b_fc2        #Basic Single dense layer with relu6

    ###### TRAIN AND EVALUATE ######
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cross_entropy)
    # train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess.run(tf.global_variables_initializer())

    for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={
                x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print("test accuracy %g" % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))


