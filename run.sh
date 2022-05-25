#!/bin/bash

python3 experimentos3_0.py FV &> fv.log &
python3 experimentos3_0.py TF_IDF &> tf_idf.log &
python3 experimentos3_0.py W2V &> w2v.log &
python3 experimentos3_0.py Features_Textuais &> feat.log &
python3 experimentos3_0.py TF_IDF_Features_Textuais &> tf.log &
python3 experimentos3_0.py FV_Features_Textuais &> fv_f.log &
python3 experimentos3_0.py W2V_Features_Textuais &> w2v_f.log &
python3 experimentos3_0.py ALL &> all.log &