import sys
sys.path.append('./evaluate_mathqa')


from fractions import Fraction
import re

from scripts.evaluate_mathqa  import find_non_numeric_answers as fn
from scripts.evaluate_mathqa import new_DataStructure as ds


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

def execute_prediction(src, pred):
    src_num_lst = get_src_numbers(src)
    temp_memory = []
    current_inst = ''
    used_num_flg = False
    used_const_flag = False
    res = None
    try:
        for pred_wd in pred.split():
            if pred_wd in ds.operation_dictionary_structure.operation_names:
                if current_inst != '':
                    ret_value = current_inst.execute()
                    if ret_value != None:
                        temp_memory.append(ret_value)
                current_inst = ds.Instruction(pred_wd)
            else:
                if current_inst == '':
                    break
                if pred_wd == 'const_pi':
                    current_inst.add_arguemnt(3.1415)
                    used_const_flag = True
                elif pred_wd == 'const_deg_to_rad':
                    current_inst.add_arguemnt(0.0055)
                    used_const_flag = True
                elif pred_wd.startswith('const_'):
                    used_const_flag = True
                    current_inst.add_arguemnt(float(pred_wd[6:]))
                elif pred_wd.startswith('#'):
                    if int(pred_wd[1:]) < len(temp_memory):
                        current_inst.add_arguemnt(temp_memory[int(pred_wd[1:])])
                elif pred_wd.startswith('n'):
                    used_num_flg = True
                    if int(pred_wd[1:]) < len(src_num_lst):
                        current_inst.add_arguemnt(src_num_lst[int(pred_wd[1:])])
                elif pred_wd != '':
                    current_inst.add_arguemnt(float(pred_wd))
            if current_inst == '':
                ans_found = False
                continue
            res = current_inst.execute()
    except Exception as e:
        print('Unable to execute target')
    return res

