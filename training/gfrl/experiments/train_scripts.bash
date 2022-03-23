#!/bin/bash

python run_multirl.py --scenario defender_hesitantdribble --mode all
python run_multirl.py --scenario defender_zigzagdribble --mode all
python run_multirl.py --scenario 2v2 --mode all
python run_multirl.py --scenario 2v2_counterattack --mode all
python run_multirl.py --scenario 2v2_highpassforward --mode all
python run_multirl.py --scenario 3v2_counterattack --mode all
python run_multirl.py --scenario 3v2_crossfromside --mode all
python run_multirl.py --scenario 3v2_sidebuildup --mode all

python run_multirl.py --scenario grf_passshoot --mode allNonGK
python run_multirl.py --scenario grf_runtoscore --mode allNonGK
python run_multirl.py --scenario grf_runpassshoot --mode allNonGK
python run_multirl.py --scenario offense_avoidpassshoot --mode allNonGK
python run_multirl.py --scenario offense_easycross --mode allNonGK
python run_multirl.py --scenario offense_hardcross --mode allNonGK
python run_multirl.py --scenario offense_11gk --mode 3

