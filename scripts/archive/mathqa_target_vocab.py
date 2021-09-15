import argparse
import re


def gen_tgt_vocab_mathqa(ip_filepath, op_filepath):
    misc_list = ['|', ')', ',']
    operations_set = set()
    arguments_set = set()

    with open(ip_filepath) as f:
        for line in f:
            for operation in line.split('|'):
                if operation != '\n':
                    operations_set.add(re.search('(.*)\(', operation).group(1) + '(')
                    arguments_set.update(re.search('\((.*)\)', operation).group(1).split(','))

    with open(op_filepath, 'w') as f:
        for item in operations_set:
            f.write('%s\n' % item)
        for item in arguments_set:
            f.write('%s\n' % item)
        for item in misc_list:
            f.write('%s\n' % item)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='Retrieve operations available in MathQa train set')

    args_parser.add_argument('ip_filepath', type=str, help='File which only contains linear_formula from math qa')
    args_parser.add_argument('op_filename', type=str,
                             help='Output file path where the operators and arguments are stored')

    args = args_parser.parse_args()
    gen_tgt_vocab_mathqa(args.ip_filepath, args.op_filename)