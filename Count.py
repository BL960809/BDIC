import csv


def decompil(onehot):
    onehot = [int(i) for i in onehot]
    index = onehot.index(1)

    return index + 1


with open('BDIC/Data/color_feature_train.csv', 'r', encoding='utf-8') as csvfile:
    color_comb, labels = [], []
    for row in csvfile.readlines():
        tmp = row.strip().split(',')
        color_comb.append(tmp[-7:-1])
        labels.append(tmp[-1])

# 生成花色子字典
color_comb_dict = {}
for comb in color_comb[0]:
    color_comb_dict[comb] = [0] * 10

# 去掉行名
color_comb, labels = color_comb[1:], labels[1:]

# 清洗数据
color_comb = ['color_type' + str(decompil(x)) for x in color_comb]
labels = [int(x) for x in labels]

# 计数
for comb, label in zip(color_comb, labels):
    color_comb_dict[comb][label] += 1

# 输出计数文件
with open('BDIC/Data/Count.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ['color_type', 'label0', 'label1', 'label2', 'label3',
              'label4', 'label5', 'label6', 'label7', 'label8', 'label9']
    writer.writerow(header)
    for type, color_lis in zip(color_comb_dict.keys(), color_comb_dict.values()):
        writer.writerow([type] + color_lis)