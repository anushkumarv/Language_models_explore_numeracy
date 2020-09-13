import json
import re
import os 

class MathQaToDrop(object):
    def __init__(self, math_dataset_json_file_path,  math_dataset_json_file_name):
        self.math_dataset_json_file_path = math_dataset_json_file_path
        self.math_dataset_json_file_name = math_dataset_json_file_name
        self.drop_qa_component_template = '''
        {
                "question": "",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": []
                },
                "query_id": "random-id",
                "validated_answers": [
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": []
                    }
                ]
            }

        '''
        self.options_key_map = {'a':0,'b':1,'c':2,'d':3,'e':4}
        self.math_datapoints_list = []
        self.drop_format_qa_pairs_list = []
        self.drop_format_dict = {'random_topic':{'passage':'','qa_pairs':self.drop_format_qa_pairs_list}}

    def parse_mathqa_file(self):
        with open(os.path.join(self.math_dataset_json_file_path, self.math_dataset_json_file_name)) as f:
            math_data = json.load(f)
        for item in math_data:
            ans = self.extract_answer(item)
            self.math_datapoints_list.append((math_data['Problem'],ans))

    def extract_answer(self, datapoint):
        options = datapoint['options'].split(',')
        correct_option = datapoint['correct']
        answer = re.sub(r'[a-z][ ][)]', '', options[self.options_key_map[correct_option]]).strip()
        return answer

    def convert_math_data_to_drop_format(self):
        for item in self.math_datapoints_list:
            drop_datapoint = json.loads(self.drop_qa_component_template)
            drop_datapoint['question'] = item[0]
            drop_datapoint['answer']['number'] = item[1]
            drop_datapoint['validated_answers'][0]['number'] = item[1]
            self.drop_format_qa_pairs_list.append(drop_datapoint)

    def write_to_file(self):
        with open(os.path.join(self.math_dataset_json_file_path, 'drop_' + self.math_dataset_json_file_name), 'w') as f:
            f.write(json.dumps(self.drop_format_dict))

    def process(self):
        self.parse_mathqa_file()
        self.convert_math_data_to_drop_format()
        self.write_to_file()
