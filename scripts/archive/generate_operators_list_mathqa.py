import argparse
import re


def generate_operators(ip_filepath, op_filepath):
    operations_set = set()

    with open(ip_filepath) as f:
        for line in f:
            for operation in line.split('|'):
                operations_set.add(operation.split('(')[0])

    with open(op_filepath, 'w') as f:
        for item in operations_set:
            f.write('%s\n' % item)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='Retrieve operations available in MathQa train set')

    args_parser.add_argument('ip_filepath', type=str, help='File which only contains linear_formula from math qa')
    args_parser.add_argument('op_filename', type=str, help='Output file path where the operations are stored')

    args = args_parser.parse_args()
    generate_operators(args.ip_filepath, args.op_filename)

# C:\\#Resources\\Injecting_Numeracy\\Language_models_explore_numeracy\\data\\MathQA\\train.json_tgt.txt  C:\\#Resources\\Injecting_Numeracy\\Language_models_explore_numeracy\\data\\MathQA\\operation_list.txt
