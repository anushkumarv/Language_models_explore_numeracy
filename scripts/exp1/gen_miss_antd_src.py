import argparse
import os
from mathqa_exp1 import read_src_data


def write_data(data, root, prefix):
    src_file = os.path.join(root, prefix + '_src.txt')
    print(src_file)
    f = open(src_file, 'w')
    for item in data:
        src = item['Problem'] + ' [SEP] ' + item['linear_formula'].replace(')|', ' ').replace('(', ' ').\
            replace(',',' ').replace(')', ' ').strip()
        f.write('%s\n' % src)
    f.close()


def main(args):
    data = read_src_data(args.src_data_json)
    write_data(data, args.target_dir, args.prefix)
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Directly convert a json to a format suitable for exp1')
    parser.add_argument('src_data_json', type=str, help='Root directory of src json [./../data/MathQA/MathQAClean/clean_test.json]')
    parser.add_argument('target_dir', type=str, help='Directory where it needs to be saved')
    parser.add_argument('prefix', type=str, help='Prefix of the name of the name of the file saved')
    args = parser.parse_args()
    main(args)