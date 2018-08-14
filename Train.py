import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import csv
import sys
sys.path.append('D:/lehui/BDIC')
from DNNModel import DNNNet


data_directory = 'BDIC/Data/'
combination_feature_train = 'combination_feature.csv'

with open(data_directory + combination_feature_train, 'r', encoding='utf-8') as file:
    comb_train, labels = [], []
    for row in file.readlines():
        tmp = row.strip().split(',')
        comb_train.append(tmp[:31])
        labels.append(tmp[31])

# shuffle
comb_train_processed = np.array(comb_train).astype('float32')
labels_processed = np.array(labels).astype('int32')
shuffled_ix = np.random.permutation(np.arange(len(comb_train_processed)))
comb_train_shuffled = comb_train_processed[shuffled_ix]
labels_shuffled = labels_processed[shuffled_ix]

# divide train set and test set
ix_cutoff = int(len(comb_train_shuffled) * 0.8)
x_train_comb, x_test_comb = comb_train_shuffled[:ix_cutoff], comb_train_shuffled[ix_cutoff:]
y_train, y_test = labels_shuffled[:ix_cutoff], labels_shuffled[ix_cutoff:]

# set DNN parameter
epochs = 2000
n_input = 31
n_label = 10
n_hidden = 25
learning_rate = 0.001

# load DNN model
DNN = DNNNet(n_input, n_label, n_hidden, n_hidden, learning_rate)

comb_train_loss, comb_test_loss, comb_test_accuracy = [], [], []

# start training
with tf.Session() as sess:
    # initialize Session
    sess.run(tf.global_variables_initializer())

    # one hot embedding
    y_train = sess.run(tf.one_hot(list(y_train), depth=10))
    y_test = sess.run(tf.one_hot(list(y_test), depth=10))

    train_dict = {DNN.input: x_train_comb, DNN.output: y_train}
    test_dict = {DNN.input: x_test_comb, DNN.output: y_test}

    for epoch in range(epochs):
        #  前向传播
        sess.run(DNN.train_step, feed_dict=train_dict)

        #  get training loss
        temp_train_loss = sess.run(DNN.loss, feed_dict=train_dict)
        comb_train_loss.append(temp_train_loss)

        #  get test loss
        temp_test_loss, prediction = sess.run([DNN.loss, DNN.logits_out], feed_dict=test_dict)
        comb_test_loss.append(temp_test_loss)

        if (epoch+1) % 100 == 0:
            print('Epoch: {}, Train Loss:{:.4}, Test Loss: {:.4}'.format(
                epoch + 1, temp_train_loss, temp_test_loss))

    comb_weight1 = sess.run(DNN.weight1)
    comb_weight2 = sess.run(DNN.weight2)
    comb_weight3 = sess.run(DNN.weight3)

    comb_weight_tmp = np.dot(comb_weight1, comb_weight2)
    comb_weight = np.dot(comb_weight_tmp, comb_weight3)

# output the weight of combination
with open(data_directory + 'comb_weight.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in comb_weight:
        writer.writerow(row)

# 绘制折线图
ite = [x+1 for x in range(epochs)]
y_train_plt = comb_train_loss
y_test_plt = comb_test_loss

plt.plot(ite, y_train_plt, label=u'Loss for train')
plt.plot(ite, y_test_plt, label=u'Loss for test')
plt.legend()  # 让图例生效
