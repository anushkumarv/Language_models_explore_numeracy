# Extract only the correctly annotated data points
python ./../clean_math_qa.py ./../../data/MathQA train.json ./../../data/MathQA/MathQAClean
python ./../clean_math_qa.py ./../../data/MathQA dev.json ./../../data/MathQA/MathQAClean
python ./../clean_math_qa.py ./../../data/MathQA test.json ./../../data/MathQA/MathQAClean