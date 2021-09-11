import argparse
import evaluate_mathqa.new_DataStructure as ds
# import evaluate_mathqa.find_non_numeric_answers as fn
import re
import math
from fractions import Fraction

numbers_in_wrods = {"one":1,"two":2,"three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "ten":10, "hundred":100, "thousand":1000 }


def is_number(word):
    word = re.sub("/", "", word)
    word = re.sub(",", "", word)
    word = re.sub("\.", "", word)
    word = re.sub("-", "", word)
    return word.isdigit() and '²' not in word and '³' not in word and '¹' not in word and ('²' not in word) and ('³' not in word) and ('¹' not in word) and('₂' not in word) and ('⁶' not in word) and ('₃' not in word) and '⁹' not in word and '⁵' not in word and '₁' not in word and '₄' not in word and '⁷' not in word and '⁴' not in word and '⁸' not in word and '₈' not in word


def to_float(word):
    word = re.sub("\.", "", word)
    word = re.sub(",", "", word)
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


def get_src_numbers(test_src_text):
    num_list = []
    test_src_text_words = test_src_text.split(' ')
    for i in range(len(test_src_text_words)):
        word = test_src_text_words[i]
        if is_number(word):
            try:
                if i> 0 and test_src_text_words[i-1] == '-':
                    num_list.append(to_float(word) * -1)
                else:
                    num_list.append(to_float(word))
            except:
                continue
    return num_list


def main(args):
    src = read_data_from_file(args.data_src)
    tgt = read_data_from_file(args.data_tgt)
    src_pred = read_data_from_file(args.data_src_pred)
    matching_ans_count = 0
    for i in range(len(src)):
        temp_memory = []
        current_inst = ''
        used_num_flg = False
        used_const_flag = False
        number_list = get_src_numbers(src[i])
        res = None
        try:
            for prediction_word in src_pred[i].split():
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
            if res is not None and is_nearly_same(float(tgt[i]), float(res)):
                matching_ans_count += 1
        except:
            print('could not execute src sent no {}'.format(i))
            continue
    print('total matched {} out of {}'.format(matching_ans_count, len(src)))


def read_data_from_file(file):
    with open(file) as f:
        data = f.readlines()
    return data


def is_nearly_same(num1, num2, threshold = 1):
    if abs(num1 - num2) < threshold:
        return True
    return False


parser = argparse.ArgumentParser(description='evaluate predictions on deep mind, when the model was trained on mathqa')
parser.add_argument('data_src', type=str, help='file with the src questions')
parser.add_argument('data_tgt', type=str, help='file with the tgt solutions')
parser.add_argument('data_src_pred', type=str, help='file with predicted logical forms')
args = parser.parse_args()
main(args)
