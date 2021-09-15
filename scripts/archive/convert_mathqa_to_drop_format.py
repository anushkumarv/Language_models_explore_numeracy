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
        """
        Reads mathqa dataset json file and extracts the datapoints in the form of [(q1,a1), (q2,a2), ..., (qn,an)]
        """
        with open(os.path.join(self.math_dataset_json_file_path, self.math_dataset_json_file_name)) as f:
            math_data = json.load(f)
        for item in math_data:
            try:
                ans = self.extract_answer(item)
                self.math_datapoints_list.append((item['Problem'], str(ans)))
            except SyntaxError as se:
                # This takes care of cases where answer is a ratio. For ex: 1:5. I am eliminating those datapoints
                print(se)
                continue
            except Exception as e:
                print(e)
                continue

    def extract_answer(self, datapoint):
        """
        extract answer from one datapoint in mathqa dataset file
        input - {
                    "Problem": "a multiple choice test consists of 4 questions , and each question has 5 answer choices . in how many r ways can the test be completed if every question is unanswered ?",
                    "Rationale": "5 choices for each of the 4 questions , thus total r of 5 * 5 * 5 * 5 = 5 ^ 4 = 625 ways to answer all of them . answer : c .",
                    "options": "a ) 24 , b ) 120 , c ) 625 , d ) 720 , e ) 1024",
                    "correct": "c",
                    "annotated_formula": "power(5, 4)",
                    "linear_formula": "power(n1,n0)|",
                    "category": "general"
                }
        output - 625   # value of the correct option
        """
        options = datapoint['options'].split(',')
        correct_option = datapoint['correct']
        # Extract the correct option
        answer = re.sub(r'[a-z][ ][)]', '', options[self.options_key_map[correct_option]]).strip()
        # Remove unwanted characters from the answer. For ex:  58 % -> 58, rs. 50 -> 50
        answer = answer[re.search('[-0-9]', answer).start():len(answer) - re.search('[0-9]', answer[::-1]).start()]
        # Evaluate the answer. For ex: 15/3 -> 5.0
        answer = eval(answer)
        return answer

    def convert_math_data_to_drop_format(self):
        """
        convert the extract question and answer pairs from math qa dataset into the format of drop dataset
        input - [(q1,a1), (q2,a2), ..., (qn,an)]
        output - { "random_id": {
            "passage": "", 
            "qa_pairs": [
                {
                    "question": "a multiple choice test consists of 4 questions , and each question has 5 answer choices . in how many r ways can the test be completed if every question is unanswered ?",
                    "answer": {
                        "number": "625",
                        "date": {"day": "","month": "","year": ""},
                        "spans": []
                    },
                    "query_id": "random_id",
                    "validated_answers": [
                        {
                            "number": "625",
                            "date": {"day": "", "month": "", "year": ""},
                            "spans": []
                        },
                    ]
                }, ... 
                ]
            }    
        """
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
