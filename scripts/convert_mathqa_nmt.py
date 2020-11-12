import json
import os
import argparse
import re


class MathQaNmt(object):

    def __init__(self, filepath, filename):
        self.filename = filename
        self.filepath = filepath
        self.src = list()
        self.tgt = list()
        self.math_data = list()

    def __load_mathqa_file(self):
        """
        Reads mathqa dataset json file and extracts the datapoints in the form of [(q1,a1), (q2,a2), ..., (qn,an)]
        """
        with open(os.path.join(self.filepath, self.filename)) as f:
            self.math_data = json.load(f)

    def __extract_src_tgt_pairs(self):
        """
        extract src and tgt sentences from the loaded math qa dictionary
        """
        for item in self.math_data:
            self.src.append(item['Problem'])
            tgt_sent = item['linear_formula']
            tgt_sent = re.sub(r'\)\|', ' ', tgt_sent)
            tgt_sent = re.sub(r'\(', ' ', tgt_sent)
            tgt_sent = re.sub(r'\)', ' ', tgt_sent)
            tgt_sent = re.sub(r',', ' ', tgt_sent)
            self.tgt.append(tgt_sent.strip())

    def __write_data(self):
        # write src data
        print('##### Writing src file at ', os.path.join(self.filepath, self.filename + '_src.txt'))
        with open(os.path.join(self.filepath, self.filename + '_src.txt'), 'w', encoding='utf8') as f:
            for item in self.src:
                f.write("%s\n" % item)
        print('##### Writing tgt file at ', os.path.join(self.filepath, self.filename + '_tgt.txt'))
        with open(os.path.join(self.filepath, self.filename + '_tgt.txt'), 'w', encoding='utf8') as f:
            for item in self.tgt:
                f.write("%s\n" % item)

    def process(self):
        self.__load_mathqa_file()
        self.__extract_src_tgt_pairs()
        self.__write_data()


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='Convert a math qa json to NMT format')

    args_parser.add_argument('filepath', type=str, help='directory of the src json path')
    args_parser.add_argument('filename', type=str, help='name of the src json file')

    args = args_parser.parse_args()
    obj = MathQaNmt(args.filepath, args.filename)
    obj.process()
