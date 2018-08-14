import tensorflow as tf


class DNNNet(object):
    def __init__(self, n_input, n_label, n_hidden1, n_hidden2, learning_rate):
        self.input = tf.placeholder(tf.float32, [None, n_input])
        self.output = tf.placeholder(tf.float32, [None, n_label])
        self.weight1 = tf.Variable(tf.truncated_normal([n_input, n_hidden1], stddev=0.1))
        self.weight2 = tf.Variable(tf.truncated_normal([n_hidden1, n_hidden2], stddev=0.1))
        self.weight3 = tf.Variable(tf.truncated_normal([n_hidden2, n_label], stddev=0.1))

        # set forward
        a1 = tf.matmul(self.input, self.weight1)
        a2 = tf.matmul(a1, self.weight2)
        self.logits_out = tf.nn.softmax(tf.matmul(a2, self.weight3))

        # loss function
        losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.logits_out, labels=self.output)
        self.loss = tf.reduce_mean(losses)

        # get accuracy
        self.accuracy = tf.reduce_mean(
            tf.cast(tf.equal(tf.argmax(self.logits_out, 1), tf.argmax(self.output, 1)), tf.float32))

        # set optimizer
        optimizer = tf.train.RMSPropOptimizer(learning_rate)
        self.train_step = optimizer.minimize(self.loss)

