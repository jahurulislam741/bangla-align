Requirements: 
- python (use Miniconda/Anaconda; the use its command prompt)
- mfa
- ffmpeg

Steps to follow; run the following commands in the terminal in sequence (On Windows, replace "/" with "\" in the filepaths): 
 
1. $ python bangla_aligner/A_generate_temp_dict.py
[This script creates a temporary dictionary and an OOV file (when found); be sure to inspect and manually correct these two files before moving to the next step.]

2. $ python bangla_aligner/B_create_temp_dict_bangla_ortho_new.py

3. $ mfa validate temp_folder_mfa_input/ temp_dict_bangla_ortho_new.dict bangla_aligner/bangla.zip 

4. $ mfa align temp_folder_mfa_input/ temp_dict_bangla_ortho_new.dict bangla_aligner/bangla.zip temp_output_tgs -t temp

5. $ python bangla_aligner/C_post_processing.py

# bangla-align

