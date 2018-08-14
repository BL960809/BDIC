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


def assignA(row, color_class_num):
    row_tmp = row.copy()
    row_tmp.sort()

    if sum([int(x) for x in row_tmp[1:]]) == 46 and color_class_num == 5:
        row[row.index('1')] = '14'

    return row


def predict(color, number):
    # get color dictionary
    color_dict = get_color_dict(color)
    color_values = list(color_dict.values())

    # Tag features of the number
    color_max_num = max(color_values)

    # get number dictionary
    number_dict = get_number_dict(number)
    num_values = list(number_dict.values())

    # Tag features of the number
    max_num = max(num_values)
    number_class_num = len([x for x in num_values if x != 0])

    # replace 'J' 'Q' 'K'
    for i in number:
        if i == 'J':
            number[number.index('J')] = '11'
        if i == 'Q':
            number[number.index('Q')] = '12'
        if i == 'K':
            number[number.index('K')] = '13'

    # assign 'A'
    if '1' in number:
        number = assignA(number, number_class_num)

    # as int
    number = [int(x) for x in number]

    # predict labels
    if color_max_num == 5:
        if sum(number) == 60:
            return 1
        elif max(number) - min(number) == 4:
            return 3
        else:
            return 7
    elif number_class_num == 5:
        if max(number) - min(number) == 4:
            return 2
        else:
            return 0
    elif number_class_num == 4:
        return 8
    elif number_class_num == 3:
        if max_num == 3:
            return 9
        else:
            return 4
    elif number_class_num == 2:
        if max_num == 4:
            return 5
        else:
            return 6


# set file path
data_directory = 'BDIC/Data/'
train = 'training-final.csv'
test = 'Semifinal-testing-final.csv'

with open(data_directory + train, 'r', encoding='utf-8') as file:
    Colors, Number, labels = [], [], []
    for row in file.readlines():
        tmp = row.strip().split(',')
        Colors.append([tmp[0], tmp[2], tmp[4], tmp[6], tmp[8]])
        Number.append([tmp[1], tmp[3], tmp[5], tmp[7], tmp[9]])
        labels.append(int(tmp[10]))

pred = [predict(color, number) for color, number in zip(Colors, Number)]

# test accuracy
i = 0
for label, pred_ in zip(labels, pred):
    if label == pred_:
        i += 1
print(i / len(labels))

# predict the test set
with open(data_directory + test, 'r', encoding='utf-8') as file:
    Colors, Number, labels = [], [], []
    for row in file.readlines():
        tmp = row.strip().split(',')
        Colors.append([tmp[0], tmp[2], tmp[4], tmp[6], tmp[8]])
        Number.append([tmp[1], tmp[3], tmp[5], tmp[7], tmp[9]])

dsjyycxds_semifinal = [predict(color, number) for color, number in zip(Colors, Number)]

# output the prediction
with open(data_directory + 'dsjyycxds_semifinal.txt', 'w', encoding='utf-8') as file:
    for row in dsjyycxds_semifinal:
        file.writelines(str(row) + '\n')




