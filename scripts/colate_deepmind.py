import argparse
import os

FILE_EXCEPTIONS_LIST = ['comparsion']
SUB_DIRS = ['train-easy', 'train-medium', 'train-hard']


def main(args):
    total_questions = list()
    total_sols = list()
    for dir in SUB_DIRS:
        files = os.listdir(os.path.join(args.dataset_root, dir))
        for file in files:
            if file not in FILE_EXCEPTIONS_LIST:
                questions, sols = extract_datapoint_file(args.dataset_root, dir, file)
                total_questions.extend(questions)
                total_sols.extend(sols)
    print('total number of questions {}'.format(len(total_questions)))
    print('total number of sols {}'.format(len(total_sols)))
    save_data_to_file(args.dataset_root, total_questions, total_sols)


def extract_datapoint_file(root, dir, file):
    abs_path = os.path.join(root, dir, file)
    with open(abs_path) as f:
        file_contents = f.readlines()
    questions = list()
    sols = list()
    dropped = 0
    for i in range(0, len(file_contents), 2):
        try:
            ans = float(file_contents[i+1].strip())
            questions.append(file_contents[i].strip())
            sols.append(ans)
        except Exception as e:
            dropped += 1
            continue
    print('total questions dropped in {} is {}'.format(file, dropped))
    return questions, sols


def save_data_to_file(dir, questions, sols):
    src_path = os.path.join(dir, 'deepmind_src.txt')
    tgt_path = os.path.join(dir, 'deepmind_tgt.txt')
    with open(src_path, 'w') as f:
        for item in questions:
            f.write(item + '\n')
    with open(tgt_path, 'w') as f:
        for item in sols:
            f.write(str(item) + '\n')


parser = argparse.ArgumentParser(description='colate deep mind data into open nmt format')
parser.add_argument('dataset_root', type=str, help='path pointing to root dir of dataset')
args = parser.parse_args()
main(args)
