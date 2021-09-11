import sys
sys.path.append('./evaluate_mathqa')

import argparse
import math
from fractions import Fraction
import json
from tqdm import tqdm
import os
import re


from evaluate_mathqa import new_DataStructure as ds
from evaluate_mathqa  import find_non_numeric_answers as fn



numbers_in_wrods = {"one":1,"two":2,"three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "ten":10, "hundred":100, "thousand":1000 }


def is_number(word):
    word = re.sub("/", "", word)
    word = re.sub(",", "", word)
    word = re.sub("\.", "", word)
    return word.isdigit() and '²' not in word and '³' not in word and '¹' not in word and ('²' not in word) and ('³' not in word) and ('¹' not in word) and('₂' not in word) and ('⁶' not in word) and ('₃' not in word) and '⁹' not in word and '⁵' not in word and '₁' not in word and '₄' not in word and '⁷' not in word and '⁴' not in word and '⁸' not in word and '₈' not in word


def to_float(word):
    if word in numbers_in_wrods:
        return numbers_in_wrods[word]
    if '/' in word:
        word_parts = word.split('/')
        if len(word_parts[0]) == 0 or len(word_parts[1]) == 0:
            word = re.sub("/", "", word)
            return float(word)
        num = Fraction(int(word_parts[0]), int(word_parts[1]))
        return float(num)
    elif ',' in word:
        word = re.sub(',', '', word)
    if '_' in word:
      word = re.sub('_', '', word)
    return float(word)


def parse_options(options):
    res_opts = []
    options = options.replace('u\'', '').replace('\"', '\'').replace('\'', '').replace(']', '').replace('[','').replace('  ', ', ').split(', ')
    for opt in options:
        if ')' not in opt:
            opt = 'a)' + opt
        res_opts.append(fn.find_non_numeric_values(opt.replace(' ', '')))
    return res_opts


def get_src_numbers(test_src_text):
    num_list = []
    test_src_text_words = test_src_text.split(' ')
    for i in range(len(test_src_text_words)):
        word = test_src_text_words[i]
        if is_number(word):
            if i> 0 and test_src_text_words[i-1] == '-':
                num_list.append(to_float(word) * -1)
            else:
                num_list.append(to_float(word))
    return num_list


def parse_data_points(data_points_lst):
    correct_formula_count = 0
    options_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    clean_data_points = []
    errored_data_points = []

    for datapoint in tqdm(data_points_lst):
        tgt_formula = datapoint['linear_formula'].replace(')|', ' ').replace('(', ' ').replace(',',' ').\
            replace(')', ' ').strip()
        options = parse_options(datapoint['options'])
        temp_memory = []
        current_inst = ''
        used_num_flg = False
        used_const_flag = False
        number_list = get_src_numbers(datapoint['Problem'])
        try:
            for prediction_word in tgt_formula.split():
                if prediction_word in ds.operation_dictionary_structure.operation_names:
                    if current_inst != '':
                        ret_value = current_inst.execute()
                        if ret_value != None:
                            temp_memory.append(ret_value)
                    current_inst = ds.Instruction(prediction_word)
                else:
                    if current_inst == '':
                        break
                    if prediction_word == 'const_pi':
                        current_inst.add_arguemnt(3.1415)
                        used_const_flag = True
                    elif prediction_word == 'const_deg_to_rad':
                        current_inst.add_arguemnt(0.0055)
                        used_const_flag = True
                    elif prediction_word.startswith('const_'):
                        used_const_flag = True
                        current_inst.add_arguemnt(float(prediction_word[6:]))
                    elif prediction_word.startswith('#'):
                        if int(prediction_word[1:]) < len(temp_memory):
                            current_inst.add_arguemnt(temp_memory[int(prediction_word[1:])])
                    elif prediction_word.startswith('n'):
                        used_num_flg = True
                        if int(prediction_word[1:]) < len(number_list):
                            current_inst.add_arguemnt(number_list[int(prediction_word[1:])])
                    elif prediction_word != '':
                        current_inst.add_arguemnt(float(prediction_word))
                if current_inst == '':
                    ans_found = False
                    continue
                res = current_inst.execute()
        except Exception as e:
            print('exception', str(e))
            print('linear formula', datapoint['linear_formula'])
            print('pred_word', prediction_word)
            break

        if res in options:
            if res == options[options_map[datapoint['correct']]]:
                correct_formula_count += 1
                clean_data_points.append(datapoint)
            else:
                errored_data_points.append(datapoint)
        else:
            errored_data_points.append(datapoint)
    return clean_data_points, errored_data_points


def read_src_data(file):
    with open(file) as f:
        data_points_lst = json.load(f)
    return data_points_lst


def convert_nmt_format(data_points):
    src_lst = list()
    tgt_lst = list()
    for item in data_points:
        src_lst.append(item['Problem'])
        tgt_lst.append(item['linear_formula'].replace(')|', ' ').replace('(', ' ').replace(',',' ').
                       replace(')', ' ').strip())

    return src_lst, tgt_lst


def write_data(data_points, prefix, args):
    if not os.path.exists(args.tgt_data_root_dir):
        os.mkdir(args.tgt_data_root_dir)
    json_write_file = os.path.join(args.tgt_data_root_dir, prefix + args.src_json)
    with open(json_write_file, 'w') as f:
        f.write(json.dumps(data_points, indent=1))
    src_lst, tgt_lst = convert_nmt_format(data_points)
    src_file = os.path.join(args.tgt_data_root_dir, prefix + args.src_json + '_src.txt')
    tgt_file = os.path.join(args.tgt_data_root_dir, prefix + args.src_json + '_tgt.txt')
    with open(src_file, 'w') as f:
        for line in src_lst:
            f.write("%s\n" % line)
    with open(tgt_file, 'w') as f:
        for line in src_lst:
            f.write("%s\n" % line)


def main(args):
    print('## Reading data ##')
    data_points_lst = read_src_data(os.path.join(args.src_data_root_dir, args.src_json))
    print('## Validating / Extracting correct data points ##')
    clean_data_points, errored_data_points = parse_data_points(data_points_lst)
    print('## Writing data ##')
    write_data(clean_data_points, 'clean_', args)
    write_data(errored_data_points, 'error_', args)
    print('Length of clean data ', len(clean_data_points))
    print('Length of errored data ', len(errored_data_points))
    print('## Completed ##')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='clean up the math qa dataset')
    parser.add_argument('src_data_root_dir', type=str, help='root directory of src data [./../data/MathQA]')
    parser.add_argument('src_json', type=str, help='name of the json file. [test.json / train.json / dev.json]')
    parser.add_argument('tgt_data_root_dir', type=str, help='name of the json file. [./../data/MathQA/MathQAClean]')
    args = parser.parse_args()
    main(args)
