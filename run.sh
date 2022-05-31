#!/bin/bash

python3 -u experimentos3_0.py FV &> logs/fv.log &
python3 -u experimentos3_0.py TF_IDF &> logs/tf_idf.log &
python3 -u experimentos3_0.py W2V &> logs/w2v.log &
python3 -u experimentos3_0.py Features_Textuais &> logs/feat.log &
python3 -u experimentos3_0.py TF_IDF_Features_Textuais &> logs/tf.log &
python3 -u experimentos3_0.py FV_Features_Textuais &> logs/fv_f.log &
python3 -u experimentos3_0.py W2V_Features_Textuais &> logs/w2v_f.log &
python3 -u experimentos3_0.py ALL &> logs/all.log &
