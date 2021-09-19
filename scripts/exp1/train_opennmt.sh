# The paths mentioned in this shell script will assume the structure of this repo. Please verify/change for independent experiments
python ../clean_math_qa.py ./../../data/MathQA train.json ./../../data/MathQA/MathQAClean
python ../clean_math_qa.py ./../../data/MathQA test.json ./../../data/MathQA/MathQAClean
python ../clean_math_qa.py ./../../data/MathQA dev.json ./../../data/MathQA/MathQAClean

# to generate the synthetic data of the form "src [SEP] incorrect symbolic expression" --> "correct symbolic expression"
python mathqa_exp1.py ./../../data/MathQA/MathQAClean clean_train.json ./../../data/MathQA/MathQAExp1 train_exp1 1
python mathqa_exp1.py ./../../data/MathQA/MathQAClean clean_test.json ./../../data/MathQA/MathQAExp1 test_exp1 1 1
python mathqa_exp1.py ./../../data/MathQA/MathQAClean clean_dev.json ./../../data/MathQA/MathQAExp1 dev_exp1 1 1

# Install OpenNMT
pip install OpenNMT-py==2.0.0rc1

# Preprocess
onmt_build_vocab -config preprocess.yaml -n_sample 10000

# Train
onmt_train -config train.yaml

# Translation
onmt_translate -model mathQaExp111TransformerLyrs1Sd3_step_6000.pt -src ./../../data/MathQA/MathQAExp1/test_exp1_1_1_src.txt -output predictions.txt -gpu 0 --beam_size 200 --n_best 50
sed -i 's/<unk>//g' predictions.txt
sed -i 's/<blank>//g' predictions.txt

# Evaluation
python evaluate_error_correction.py ./../../data/MathQA/MathQAClean/clean_test.json ./../../data/MathQA/MathQAExp1/test_exp1_1_1_src.txt predictions.txt 50