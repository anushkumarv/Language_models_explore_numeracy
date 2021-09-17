# The paths mentioned in this shell script will assume the structure of this repo. Please verify/change for independent experiments



# Install OpenNMT
pip install OpenNMT-py==2.0.0rc1

# Preprocess
onmt_build_vocab -config preprocess.yaml -n_sample 10000

# Train
onmt_train -config train.yaml