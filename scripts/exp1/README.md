## Introduction
The idea is to  automatically correct the miss-annotated data points from MathQA dataset
### Steps 
* Install OpenNMT <br>
```
pip install OpenNMT-py==2.0.0rc1
```

* Extract/ filter only those data points which were annotated correctly. In other words clean up the dataset
  * The below scripts takes the arguments 
    * Directory in which MathQA data set is saved 
    * Name of the file that needs to be processed 
    * The target directory in which the processed/filtered data needs to be saved containing only the correctly annotated data 
```
python ../clean_math_qa.py ./../../data/MathQA train.json ./../../data/MathQA/MathQAClean
python ../clean_math_qa.py ./../../data/MathQA dev.json ./../../data/MathQA/MathQAClean
python ../clean_math_qa.py ./../../data/MathQA test.json ./../../data/MathQA/MathQAClean
```

* Synthetically generate data of the form "src [SEP] incorrect symbolic expression" --> "correct symbolic expression"
  * The script takes the arguments 
    * Path to the directory containing the cleaned up data set (mentioned in the earlier step)
    * Name of the file that needs to be processed
    * Directory under which the processed data needs to be saved
    * Give a prefix that needs to appended to the file saved
    * Rate of corruption - For a given src, indicate the number of times the symbolic expression needs to be corrupted
      * For example - lets say that the number is 2, then the processed data will be 
        * src [SEP] incorrect tgt1 -> correct tgt
        * src [SEP] incorrect tgt2 -> correct tgt
```
python mathqa_exp1.py ./../../data/MathQA/MathQAClean clean_train.json ./../../data/MathQA/MathQAExp1 train_exp1 1
python mathqa_exp1.py ./../../data/MathQA/MathQAClean clean_test.json ./../../data/MathQA/MathQAExp1 test_exp1 1 1
python mathqa_exp1.py ./../../data/MathQA/MathQAClean clean_dev.json ./../../data/MathQA/MathQAExp1 dev_exp1 1 1
```
* Train your model
  * Make sure you have edited the preprocess.yaml and train.yaml according to needs
```
onmt_build_vocab -config preprocess.yaml -n_sample 10000
onmt_train -config train.yaml
```
* Predict on test data (which was generated on step 2) (eventually we will need to test on the mis annotated data)
  * The name of the model will take the form <name in train.yaml>_step_<epoch>.pt
  * n_best will give you n predictions per src

```
onmt_translate -model mathQaExp111TransformerLyrs1Sd3_step_2000.pt -src ./../../data/MathQA/MathQAExp1/test_exp1_1_1_src.txt -output predictions.txt -gpu 0 --beam_size 200 --n_best 50
sed -i 's/<unk>//g' models/mathQaExp113TransformerLyrs1Sd3/predictions.txt
sed -i 's/<blank>//g' models/mathQaExp113TransformerLyrs1Sd3/predictions.txt
```
* Evaluate your predictions. The arguments taken will be 
  * The test json file which we generated in step 2
  * Path to the source file
  * Path to the predictions file
  * number of predictions per data point (n_best from previous step)
```
python evaluate_error_correction.py ./../../data/MathQA/MathQAClean/clean_test.json ./../../data/MathQA/MathQAExp1/test_exp1_1_1_src.txt predictions.txt 50
```
 