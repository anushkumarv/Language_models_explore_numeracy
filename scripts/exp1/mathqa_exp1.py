import argparse
import json
from tqdm import tqdm
import random
import os
import re

from scripts.clean_math_qa import get_src_numbers

with open('operations.txt') as f:
    operations = f.readlines()
# Process to remove new line characters 'add\n' to 'add'
operations = [item.strip() for item in operations]

with open('constants.txt') as f:
    contants = f.readlines()
# Process to remove new line characters 'add\n' to 'add'
contants = [item.strip().lower() for item in contants]


def read_src_data(file):
    with open(file) as f:
        data_points_lst = json.load(f)
    return data_points_lst


def process_tgt(tgt_lst, num_in_q):
    # Choose how many change would we like to make
    if len(tgt_lst) > 3:
        # num_chngs = random.randint(1, len(tgt_lst) - 2)
        num_chngs = random.randint(1, 3)
    else:
        num_chngs = 1
    # Sample the indices from the tgt list where we like to make changes
    chng_idx = random.sample(range(len(tgt_lst)), num_chngs)
    for i in chng_idx:
        op = tgt_lst[i]
        # Check if the instruction we are trying to change is a function or an argument and handle accordingly
        if op in operations:
            # Replace it by a random operation/ function from the supported operations list
            # TODO : check if the number of arguments to the operation/function is the same
            tgt_lst[i] = random.sample(operations, 1)
        elif op[0] == '#':
            # Check how many operation functions preceeded the argument to determine to which number can it perturbed
            # add(n0,const_1)|add(#0,const_1)|add(#0,#1)|
            n_op_bfr = len([tgt_lst[j] for j in range(i) if tgt_lst[j] in operations]) - 1
            tgt_lst[i] = '#' + str(random.randint(0, n_op_bfr))
        elif len(op) == 2 and op[0] == 'n':
            # The number argument replaced must be available within the question
            tgt_lst[i] = 'n' + str(random.randint(0, len(num_in_q) - 1))
        elif op.startswith('const_'):
            # Replace it by a random constant number from the supported list
            tgt_lst[i] = random.sample(contants, 1)
        else:
            continue
    return tgt_lst


def process_datapoint(data_point, rate_of_corruption):
    new_src, new_tgt = list(), list()
    for _ in range(rate_of_corruption):
        src = data_point['Problem']
        tgt = data_point['linear_formula'].replace(')|', ' ').replace('(', ' ').replace(',',' ').\
            replace(')', ' ').strip()
        tgt_lst = tgt.split()
        num_in_q = get_src_numbers(src)
        temp_tgt = process_tgt(tgt_lst, num_in_q)
        new_src.append(src + ' [SEP] ' + ' '.join(temp_tgt))
        new_tgt.append(tgt)
    return new_src, new_tgt


def create_pairs(data_points_lst, rate_of_corruption):
    src = list()
    tgt = list()
    for item in tqdm(data_points_lst):
        new_src, new_tgt = process_datapoint(item, rate_of_corruption)
        src.extend(new_src)
        tgt.extend(new_tgt)
    return src, tgt


def write_data(src, tgt, args):
    if not os.path.exists(args.tgt_data_root_dir):
        os.mkdir(args.tgt_data_root_dir)
    file_src = os.path.join(args.tgt_data_root_dir, args.prefix + '_src.txt')
    with open(file_src, 'w') as f:
        for line in src:
            f.write("%s\n" % line)
    file_tgt = os.path.join(args.tgt_data_root_dir, args.prefix + '_tgt.txt')
    with open(file_tgt, 'w') as f:
        for line in tgt:
            f.write("%s\n" % line)


def main(args):
    print('## Reading data ##')
    data_points_lst = read_src_data(os.path.join(args.src_data_root_dir, args.src_json))
    print('## Processing data ##')
    src, tgt = create_pairs(data_points_lst, args.rate_of_corruption)
    print('## Writing data ##')
    write_data(src, tgt, args)
    print('## Completed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='clean up the math qa dataset')
    parser.add_argument('src_data_root_dir', type=str, help='root directory of src data [./../../data/MathQA/MathQAClean]')
    parser.add_argument('src_json', type=str, help='name of the json file. [clean_test.json / clean_train.json / clean_dev.json]')
    parser.add_argument('tgt_data_root_dir', type=str, help='name of the json file. [./../../data/MathQA/MathQAExp1]')
    parser.add_argument('prefix', type=str, help='prefix used to store the generated files [test_exp1 / train_exp1 / dev_exp1]')
    parser.add_argument('rate_of_corruption', type=int, help='number of incorrect translations per datapoint')
    args = parser.parse_args()
    main(args)
