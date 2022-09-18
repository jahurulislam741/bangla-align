
'''
THIS SCRIPT...
GENERATES PHONEME DICTIONARY; CREATES TRANSLITERATED TEXTGRIDS
INPUT: SCRIPT TAKES ONE ARGUMENT-A FOLDERNAME CONTAINING THE TRANSCRIPTION TEXTGRIDS
OUTPUT: 2 FILES: A) 
'''

from my_functions import *  # import my functions
import glob  # for making a list of files in a folder
import os
import shutil
import sys
from pathlib import Path

# script_file = sys.argv[0]
# folder_name = sys.argv[1]  # the input folder name must be the first argument of this script

folder_name = 'input_audio_and_transcription_tgs' # when script is run from terminal and home-dir is bangla-aligner-linux
file_paths = glob.glob(folder_name + "/*.TextGrid")

# read the words from the TextGrid files
words_from_all_textgrids = []
for f_path in file_paths:
    with open(f_path, 'r', encoding='UTF-8')as fr:
        # make a list of words in the textgrid
        text_lines = fr.readlines()
        words_in_this_file = list_words_from_texgrid(text_lines)
        for word in words_in_this_file:
            words_from_all_textgrids.append(word + '\n')

# tokenize to words and sort
words_in_transcription_files = sorted(tokenize_to_words(words_from_all_textgrids))

# check if the words in the transcription files are available in the existing phoneme dictionary
dict_name = 'files_required_for_scripts/master_phoneme_dictionary.txt'
with open(dict_name, 'r', encoding='UTF-8')as fr:
    # read in the lines in the file
    words_in_master_dict = []
    temp_dict_bangla_ortho = []
    out_of_voc = []
    text_lines_in_dict = fr.readlines()
    for line in text_lines_in_dict[1:]:
        x = line[:-1].split('   ')
        words_in_master_dict.append(x[0])

    for word in sorted(words_in_transcription_files):
        if word in words_in_master_dict:
            index = words_in_master_dict.index(word)
            indices = [i for i, x in enumerate(words_in_master_dict) if x == word]
            for i in indices:
                y = text_lines_in_dict[i+1].split('   ')
                new_line_bangla_ortho = str(y[0]) + '   ' + str(y[1])
                temp_dict_bangla_ortho.append(new_line_bangla_ortho)
        else:
            out_of_voc.append(word)

# PROCESSING OUT OF VOCABULARY (OOV) ITEMS
if len(out_of_voc) > 0:
    oov = out_of_voc
    oov = map_consonants(oov) # map exceptional consonant pronunciations
    oov = map_vowels(oov) # map exceptional vowel pronunciations
    oov_with_phoneme_suggestions = map_grapheme_to_phoneme(oov) # map grapheme to phoneme
    # for item in oov_with_phoneme_suggestions:
    #     new_line = item + '\n'
    #     temp_dict_bangla_ortho.append(new_line)

    # write the entries to a file
    with open('oov_with_phoneme_suggestions.txt', 'w', encoding='UTF-8') as fw:
        fw.writelines(''.join(i) + '\n' for i in sorted(set(oov_with_phoneme_suggestions)))
    print("\n# ----------------------------------------------------------------")
    print('OOVs found! Listed in "oov_with_phoneme_suggestions.txt"')
    #print('Edit the entries in this file, and add them to "temp_dictionary.dict"')
    print("# ----------------------------------------------------------------\n")
else:
    #print('No OOV found!')
    print(' ')

# write the new dictionary to be used with the forced aligner
with open('temp_dict_bangla_ortho.dict', 'w', encoding='UTF-8') as fw:
    fw.writelines(''.join(i) for i in sorted(set(temp_dict_bangla_ortho)))
    print('"temp_dict_bangla_ortho.dict" generated')

print(' ')
print('NEXT STEP:')
print('Check "temp_dict_bangla_ortho.dict" and "oov_with_phoneme_suggestions.txt" (if generated in the current directory), and correct any errors before running the mfa_align script')
print('')




