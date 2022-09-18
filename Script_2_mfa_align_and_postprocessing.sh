#!/bin/bash

# generate modified dictionary file
python3 bangla_aligner/B_create_temp_dict_bangla_ortho_new.py 

# do the alignment
echo Alignment process begins...
bangla_aligner/mfa-bin-linux-1.1.0-beta2/mfa_align temp_folder_mfa_input/ temp_dict_bangla_ortho_new.dict bangla_aligner/bangla.zip temp_output_tgs -t temp

# post processing
echo ''
echo Post-processing ...
echo ''
python3 bangla_aligner/C_post_processing.py

