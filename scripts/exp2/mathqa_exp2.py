import argparse
from random import random
from random import sample
from random import randint
from scripts.exp1.mathqa_exp1 import MathQAExp1

operations = list()
contants = list()


def read_contants():
    global operations, contants
    with open('./../exp1/operations.txt') as f:
        operations = f.readlines()
    # Process to remove new line characters 'add\n' to 'add'
    operations = [item.strip() for item in operations]

    with open('./../exp1/constants.txt') as f:
        contants = f.readlines()
    # Process to remove new line characters 'add\n' to 'add'
    contants = [item.strip().lower() for item in contants]


class MathQAExp2(MathQAExp1):

    @staticmethod
    def flip(p):
        return 1 if random() < p else 0

    def process_tgt(self, tgt_lst, num_in_q, num_incorrect_tokens):

        # Decide whether to perturb it or not based on a weighted probability
        # This will ensure that some of the data points are kept clean
        if not self.flip(0.7):
            return tgt_lst

        # Choose how many change would we like to make
        if len(tgt_lst) > 3:
            # num_chngs = random.randint(1, len(tgt_lst) - 2)
            # num_chngs = random.randint(1, 3)
            num_chngs = num_incorrect_tokens
        else:
            num_chngs = 1
        # Sample the indices from the tgt list where we like to make changes
        chng_idx = sample(range(len(tgt_lst)), num_chngs)
        for i in chng_idx:
            op = tgt_lst[i]
            # Check if the instruction we are trying to change is a function or an argument and handle accordingly
            if op in operations:
                # Replace it by a random operation/ function from the supported operations list
                # TODO : check if the number of arguments to the operation/function is the same
                tgt_lst[i] = sample(operations, 1)[0]
            elif op[0] == '#':
                # Check how many operation functions preceeded the argument to determine to which number can it perturbed
                # add(n0,const_1)|add(#0,const_1)|add(#0,#1)|
                n_op_bfr = len([tgt_lst[j] for j in range(i) if tgt_lst[j] in operations]) - 1
                tgt_lst[i] = '#' + str(randint(0, n_op_bfr))
            elif len(op) == 2 and op[0] == 'n':
                # The number argument replaced must be available within the question
                tgt_lst[i] = 'n' + str(randint(0, len(num_in_q) - 1))
            elif op.startswith('const_'):
                # Replace it by a random constant number from the supported list
                tgt_lst[i] = sample(contants, 1)[0]
            else:
                continue
        return tgt_lst


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='insert random perturbations for the target symbolic expression')
    parser.add_argument('src_data_root_dir', type=str, help='root directory of src data [./../../data/MathQA/MathQAClean]')
    parser.add_argument('src_json', type=str, help='name of the json file. [clean_test.json / tr_clean_train.json / dv_clean_train.json]')
    parser.add_argument('tgt_data_root_dir', type=str, help='name of the json file. [./../../data/MathQA/MathQAExp1]')
    parser.add_argument('prefix', type=str, help='prefix used to store the generated files [test_exp1 / train_exp1 / dev_exp1]')
    parser.add_argument('rate_of_corruption', type=int, help='number of incorrect translations per datapoint')
    parser.add_argument('num_incorrect_tokens', type=int, help='number of incorrect tokens per data points')
    args = parser.parse_args()
    read_contants()
    obj = MathQAExp2()
    obj.main(args)
