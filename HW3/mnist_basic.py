from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

# dataset, because we need data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# tensorflow interactive session, the connection to the C++ backend
sess = tf.InteractiveSession()

# placeholders
# x is input tensor as a placehodler, 784 is the dimensionality of a 28x28 image
# y is the output, its shape being the dimensionality of the set of potential outputs, 0-9
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

# variables
# W are the weights, a 784x10 matrix
# b are our biases, of dimensonality 10 as we have 10 classes 0-9
# both being intialized as full 0's for our network
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

# NOTE: must be initialized with values prior to use by the session
sess.run(tf.global_variables_initializer())

# implement regression model
# vectorized image, times weights, plus bias
y = tf.matmul(x,W) + b

# define the loss function
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))

# train the model

# gradiant decent with a step length of 0.5, decends cross_entropy
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# 100 training examples for each iteration
# run train_step operation using feed_direct to fill placeholders x and y_
# NOTE: can replace any tensor with feed_direct!
for _ in range(1000):
  batch = mnist.train.next_batch(100)
  train_step.run(feed_dict={x: batch[0], y_: batch[1]})


# Evaluate the model

# check prediction
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

# determinte accuracy based on correct predictions
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# evaluate accuracy
print(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

# 0.9193, 0.918, 0.9176, 0.9185, 0.9173
# basically this sucks, can't even hit the 0.92 expected accuracy for this primative network, which is still horrible
