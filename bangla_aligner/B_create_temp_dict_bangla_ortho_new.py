'''
THIS SCRIPT...
1. COMBINES ENTRIES FROM TWO DICTIONARIES: A) 'temp_dict_bangla_ortho.dict' AND B) 'oov_with_phoneme_suggestions.txt', AFTER THEY HAVE BEEN MANUALLY INSPECTED FOR ERRORS
2. CREATES A NEW SET OF TRANSCRIPTION TEXTGRIDS BY REPLACING THE WORD-FINAL DIACRITICS (MFA
SOMEHOW CONSIDERS THEM AS PUNCTUATIONS AND REMOVES THEM OTHERWISE)
3. CREATES A TEMPORARY FOLDER NAMED 'temp_folder_mfa_input' AND STORES THE AUDIO AND TEXGRIDS IN IT
4. REMOVES TEMP FILES/FOLDERS FROM PREVIOUS INTERATION OF THE ALIGNER
'''

from my_functions import *  # import my functions
import glob  # for making a list of files in a folder
import shutil
import os.path

###################################################
# WRITE A NEW TEMP DICTIONARY ADDING AN 'X' TO EACH BANGLA WORD (TO PREVENT MFA ALIGNER FROM CONSIDERING SOME WORD-FINAL DIACRITICS AS PUNCUTATIONS)
filename = 'temp_dict_bangla_ortho.dict'
with open(filename, 'r', encoding='UTF-8')as fr:
    # read in the lines in the file
    temp_dict_bangla_ortho_new = []
    text_lines_in_dict = fr.readlines()
    for line in text_lines_in_dict:
        line_split = line.split('   ')
        word_orginal = line_split[0]
        #word_new = replace_word_final_vowel_diacritic(word_orginal)
        word_new = word_orginal + 'x'
        result = word_new + '   ' + line_split[1]
        temp_dict_bangla_ortho_new.append(result)

# add out-of-vocabulary words to the new temp dict
oov_file = 'oov_with_phoneme_suggestions.txt'
if os.path.exists(oov_file):
    with open(oov_file, 'r', encoding='UTF-8')as fr:
        # read in the lines in the file
        text_lines_in_dict = fr.readlines()
        for line in text_lines_in_dict:
            line_split = line.split('   ')
            word_orginal = line_split[0]
            # word_new = replace_word_final_vowel_diacritic(word_orginal)
            word_new = word_orginal + 'x'
            result = word_new + '   ' + line_split[1]
            temp_dict_bangla_ortho_new.append(result)

with open('temp_dict_bangla_ortho_new.dict', 'w', encoding='UTF-8') as fw:
    fw.writelines(''.join(i) for i in sorted(set(temp_dict_bangla_ortho_new)))
    print('')
    print('"temp_dict_bangla_ortho_new.dict" generated')
    print('')




##################################################
# # create a folder to store intermediate files in the aligning process
temp_dir = 'temp_folder_mfa_input'
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)  # delete earlier copy, if exists
os.makedirs(temp_dir)

###################################################
# CREATE MODIFIED TEXTGRIDS REPLACING WORD-FINAL DIACRITICS WITH ENGLISH SYMBOLS
# read the words from the TextGrid files
file_names = glob.glob("input_audio_and_transcription_tgs/*.TextGrid")

for file in file_names:  # loop through all texgrid files
    new_file_name = file.split('/')[1]  # define name of new file to be written
    with open(file, 'r', encoding='UTF-8')as fr:
        lines_in_texgrid = fr.readlines()  # read the lines in texgrid file
        new_lines = add_X_word_finally_in_TGs(lines_in_texgrid)  # make a list of modified lines with transliteration
    # write the modified textgrid file
    with open('temp_folder_mfa_input/' + new_file_name, 'w', encoding='UTF-8') as fw:  # write output TextGrid file
        fw.writelines(''.join(i) for i in new_lines)


###################################################
# copy the wave files to temp_folder_mfa_input
wave_files =  glob.glob("input_audio_and_transcription_tgs/*.wav")
for f in wave_files:
    shutil.copy(f, 'temp_folder_mfa_input')


# DELETE PREVIOUS 'TEMP' FOLDER
temp_dir = 'temp'
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)  # delete earlier copy, if exists

# DELETE PREVIOUS 'MFA' FOLDER
temp_dir = '/home/jahir/Documents/MFA'
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)  # delete earlier copy, if exists


