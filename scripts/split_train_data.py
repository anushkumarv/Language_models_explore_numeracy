import argparse
import os
from random import sample


def read_data(file):
    with open(file) as f:
        data = f.readlines()
    return data


def split_data(src_len):
    indices = [i for i in range(src_len)]
    tr_indices = sample(indices, int(0.9*src_len))
    dv_indices = list(set(indices) - set(tr_indices))
    return tr_indices, dv_indices


def write_to_file(data, file, indices ):
    with open(file, 'w') as f:
        for idx in indices:
            f.write(data[idx])


def write_data(tr_indices, dv_indices, src_data, tgt_data, args):
    tr_src = 'tr_' + args.src_train_file
    tr_tgt = 'tr_' + args.tgt_train_file
    dv_src = 'dv_' + args.src_train_file
    dv_tgt = 'dv_' + args.tgt_train_file
    write_to_file(src_data, os.path.join(args.dir, tr_src), tr_indices)
    write_to_file(tgt_data, os.path.join(args.dir, tr_tgt), tr_indices)
    write_to_file(src_data, os.path.join(args.dir, dv_src), dv_indices)
    write_to_file(tgt_data, os.path.join(args.dir, dv_tgt), dv_indices)


def main(args):
    print('## Read data ##')
    src_data = read_data(os.path.join(args.dir, args.src_train_file))
    tgt_data = read_data(os.path.join(args.dir, args.tgt_train_file))
    print('## Split data ##')
    tr_indices, dv_indices = split_data(len(src_data))
    print('## writing data ##')
    write_data(tr_indices, dv_indices, src_data, tgt_data, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='split train data into train and dev')
    parser.add_argument('dir', type=str, help='directory where files are to be read')
    parser.add_argument('src_train_file', type=str, help='src train data file')
    parser.add_argument('tgt_train_file', type=str, help='tgt train data file')
    args = parser.parse_args()
    main(args)
