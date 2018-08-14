import csv
import itertools


def get_color_dict(row):
    # create an empty dictionary
    color_dict = {}
    for color in ['H', 'S', 'D', 'C']:
        color_dict[color] = 0

    # stat frequency of each color
    for color2 in row:
        color_dict[color2] += 1

    return color_dict


def get_number_dict(row):
    # create an empty dictionary
    number_dict = {}
    for number in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        number_dict[number] = 0

    # stat frequency of each color
    for number2 in row:
        number_dict[number2] += 1

    return number_dict


def get_color_feature(row):
    # get color dictionary
    color_dict = get_color_dict(row)
    values = list(color_dict.values())

    # Tag features of the number
    max_num = max(values)
    min_num = min([x for x in values if x != 0])
    color_class_num = len([x for x in values if x != 0])

    # Tag features of different combinations
    color_type = [0] * 6    # create a zero vector
    if color_class_num == 1:
        color_type[0] = 1   # case 1: 5 x 1
    elif color_class_num == 2:
        if max_num == 4:
            color_type[1] = 1   # case 2: 4 + 1
        else:
            color_type[2] = 1   # case 3: 3 + 2
    elif color_class_num == 3:
        if max_num == 3:
            color_type[3] = 1   # case 4: 3 + 1 + 1
        else:
            color_type[4] = 1   # case 5: 2 + 2 + 1
    else:
        color_type[5] = 1   # case 6: 2 + 1 + 1 + 1

    # create feature vector
    feature = values + [max_num] + [min_num] + [color_class_num] + color_type

    return feature


def assignA(row, color_class_num):
    row_tmp = row.copy()
    row_tmp.sort()

    if sum([int(x) for x in row_tmp[1:]]) == 46 and color_class_num == 5:
        row[row.index('1')] = '14'

    return row


def get_number_feature(row):
    # get number dictionary
    number_dict = get_number_dict(row)
    values = list(number_dict.values())

    # Tag features of the number
    max_num = max(values)
    min_num = min([x for x in values if x != 0])
    number_class_num = len([x for x in values if x != 0])

    # replace 'J' 'Q' 'K'
    for i in row:
        if i == 'J':
            row[row.index('J')] = '11'
        if i == 'Q':
            row[row.index('Q')] = '12'
        if i == 'K':
            row[row.index('K')] = '13'

    # assign 'A'
    if '1' in row:
        row = assignA(row, number_class_num)

    # as int
    row = [int(x) for x in row]

    # Tag features of different number
    number_type = [0] * 8
    if number_class_num == 5:
        if max(row) - min(row) == 4:
            if sum(row) == 60:
                number_type[7] = 1      # case 8: 1 x 5   '10 + J + Q + K + A'
            else:
                number_type[6] = 1      # case 7: 1 x 5 continuous but not '10 + J + Q + K + A'
        else:
            number_type[5] = 1      # case 6: 1 x 5
    elif number_class_num == 4:
        number_type[4] = 1      # case 5: 2 + 1 + 1 + 1
    elif number_class_num == 3:
        if max_num == 3:
            number_type[3] = 1      # case 4: 3 + 1 + 1
        else:
            number_type[2] = 1      # case 3: 2 + 2 + 1
    elif number_class_num == 2:
        if max_num == 3:
            number_type[1] = 1  # case 2: 3 + 2
        else:
            number_type[0] = 1  # case 1: 4 + 1

    number_feature = values + [max_num] + [min_num] + [max(row)] + [min(row)] + \
                     [number_class_num] + [max(row) - min(row)] + number_type

    return number_feature


# set file path
data_directory = 'BDIC/Data/'
train = 'training-final.csv'
color_feature_train = 'color_feature_train.csv'
number_feature_train = 'number_feature_train.csv'

with open(data_directory + train, 'r', encoding='utf-8') as file:
    Colors, Number, labels = [], [], []
    for row in file.readlines():
        tmp = row.strip().split(',')
        Colors.append([tmp[0], tmp[2], tmp[4], tmp[6], tmp[8]])
        Number.append([tmp[1], tmp[3], tmp[5], tmp[7], tmp[9]])
        labels.append(tmp[10])

# get feature
color_feature = [get_color_feature(x) for x in Colors]
number_feature = [get_number_feature(x) for x in Number]

# output feature file
with open(data_directory + color_feature_train, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ['H_num', 'S_num', 'D_num', 'C_num', 'max_num', 'min_num', 'color_class_num',
              'color_type1', 'color_type2', 'color_type3', 'color_type4', 'color_type5', 'color_type6', 'labels']
    writer.writerow(header)
    for i in range(len(color_feature)):
        row = color_feature[i] + [int(labels[i])]
        writer.writerow(row)

with open(data_directory + number_feature_train, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ['1_num', '2_num', '3_num', '4_num', '5_num', '6_num', '7_num', '8_num', '9_num', '10_num',
              'J_num', 'Q_num', 'K_num', 'max_num', 'min_num', 'maximum_number', 'minimum_number', 'color_class_num',
              'poor_number', 'number_type1', 'number_type2', 'number_type3', 'number_type4', 'number_type5',
              'number_type6', 'number_type7', 'number_type8', 'labels']
    writer.writerow(header)
    for i in range(len(number_feature)):
        row = number_feature[i] + [int(labels[i])]
        writer.writerow(row)

# get combination feature
color_comb = [x[-6:] for x in color_feature]
number_comb = [x[-8:] for x in number_feature]
all_comb = []

# get cartesian product
for x, y in zip(color_comb, number_comb):
    cartesian = list(itertools.product(x, y))
    cartesian = [x[0] * x[1] for x in cartesian]
    all_comb.append(cartesian)

# transpose list to get rid of irrelevant columns
all_comb_transpose = [[row[i] for row in all_comb] for i in range(len(all_comb[0]))]

all_comb_final_tmp, rid_id = [], []
for i in range(len(all_comb_transpose)):
    if 1 not in all_comb_transpose[i]:
        rid_id.append(i+1)
    else:
        all_comb_final_tmp.append(all_comb_transpose[i])

all_comb_final = [[row[i] for row in all_comb_final_tmp] for i in range(len(all_comb_final_tmp[0]))]

# output the new feature
with open(data_directory + 'combination_feature.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(labels)):
        row = all_comb_final[i] + [int(labels[i])]
        writer.writerow(row)







