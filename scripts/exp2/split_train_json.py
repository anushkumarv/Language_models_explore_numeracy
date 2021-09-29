import sys

import argparse
import json
from scripts.common import read_src_data
import os
from random import sample


def sample_tr_dv_indices(data_points_lst):
    indices = [i for i in range(len(data_points_lst))]
    tr_indices = sample(indices, int(0.7*len(data_points_lst)))
    dv_indices = list(set(indices) - set(tr_indices))
    return tr_indices, dv_indices


def extract_data(indices, data_points_lst):
    data = list()
    for i in indices:
        data.append((data_points_lst[i]))
    return data


def write_data(file, data):
    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=1))


def main(args):
    print('## Reading data ##')
    data_points_lst = read_src_data(os.path.join(args.train_data_root_dir, args.train_json))
    print('## Splitting data ##')
    tr_indices, dv_indices = sample_tr_dv_indices(data_points_lst)
    tr_data = extract_data(tr_indices, data_points_lst)
    dv_data = extract_data(dv_indices, data_points_lst)
    print('## Writing data ##')
    write_data(os.path.join(args.train_data_root_dir, 'tr_' + args.train_json), tr_data)
    write_data(os.path.join(args.train_data_root_dir, 'dv_' + args.train_json), dv_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split the training set into train and dev set ')
    parser.add_argument('train_data_root_dir', type=str, help='root directory of src data [./../../data/MathQA/MathQAClean]')
    parser.add_argument('train_json', type=str, help='name of the json file. [clean_train.json]')
    args = parser.parse_args()
    main(args)
