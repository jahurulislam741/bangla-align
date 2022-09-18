

1. Place the audio and their corresponding transcription TextGrids inside the folder "input_audio_and_transcription_tgs"

2. Start a terminal window and change directory to "bangla-align***"

3. type the following command in the terminal to run run Script_1***
    $ bash Script_1_generate_dictionary.sh

4. A file named "temp_dict_bangla_ortho.dict" will be generated; inspect this file and correct any error in pronunciation of any word

5. If any word was not found in the master phoneme dictionary, another file named "oov_with_suggestions.txt" will also be generated; inspect this file and correct errors

6. 3. type the following command in the terminal to run run Script_2***
    $ bash Script_2_mfa_align_and_postprocessing.sh

7. The final output TextGrids will be generated under a new folder named "Z_final_aligned_tgs"




# bangla-align
# bangla-align
