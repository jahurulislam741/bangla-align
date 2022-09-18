'''
THIS SCRIPT...
1. REMOVES THE 'X' CHARACTERS FROM THE ALIGNGED TEXTGRID FILES
2. APPENDS THE MANUALLY CORRECTED DICTIONARY ENTRIES FOR OOV WORDS (IF ANY) TO THE
MASTER PHONEME DICTIONARY ("files_required_for_scripts/master_phoneme_dictionary.txt") 
3. REMOVES THE TEMPORARY INTERMEDIATE FILES CREATED DURING EARLIERS STEPS
'''

from my_functions import *  # import my functions
import glob  # for making a list of files in a folder
import shutil

# create a folder to store the final force-aligned TGs
final_tgs_path = 'Z_final_aligned_tgs'
if os.path.exists(final_tgs_path):
    shutil.rmtree(final_tgs_path)  # delete earlier copy, if exists
os.makedirs(final_tgs_path)

# DELET THE WORD-FINAL 'x' CHARACTER THAT WAS ADDED AT EARLIER STAGE
# read the filenames
file_names = glob.glob("temp_output_tgs/*.TextGrid")

for file in file_names:  # loop through all texgrid files
    new_file_name = file.split('/')[1]  # define name of new file to be written
    with open(file, 'r', encoding='UTF-8')as fr:
        lines_in_texgrid = fr.readlines()  # read the lines in texgrid file
        new_tg_lines = []
        for line in lines_in_texgrid:
            new_line = line.replace('x"', '"')
            new_tg_lines.append(new_line)

    # write the modified textgrid file
    with open(final_tgs_path + '/' + new_file_name, 'w', encoding='UTF-8') as fw:  # write output TextGrid file
        fw.writelines(''.join(i) for i in new_tg_lines)


###################################################
# INSERT CORRECTED WORDS IN THE MASTER PHONEME DICT
# list the words in corrected dict (temp)
filename = 'temp_dict_bangla_ortho_new.dict'
with open(filename, 'r', encoding='UTF-8')as fr:
    # read in the lines in the file
    corrected_words = []
    lines_in_corrected_dict = fr.readlines()
    for line in lines_in_corrected_dict:
        line_split = line.split('   ')
        w = line_split[0]
        word = w[:-1]
        corrected_words.append(word)

# list words in master phoneme dict
path_to_master_phoneme_dict = 'files_required_for_scripts/master_phoneme_dictionary.txt'
with open(path_to_master_phoneme_dict, 'r', encoding='UTF-8')as fr:
    # read in the lines in the file
    words_in_master_dict = []
    lines_in_master_dict = fr.readlines()
    for line in lines_in_master_dict:
        line_split = line.split('   ')
        w = line_split[0]
        word = w
        words_in_master_dict.append(word)

for word in corrected_words:
    ind_corrected_word = corrected_words.index(word)
    result = lines_in_corrected_dict[ind_corrected_word]
    result = result.replace('x', '')
    if word in words_in_master_dict:
        ind_master_dict_word = words_in_master_dict.index(word)
        lines_in_master_dict[ind_master_dict_word] = result
    else:
        lines_in_master_dict.append(result)


# UPDATE MASTER PHONEME DICT WITH THE NEW AS WELL AS CORRECTED ENRIES IN THE TEMPORARY DICTORY
with open(path_to_master_phoneme_dict, 'w', encoding='UTF-8') as fw:
    fw.writelines(''.join(i) for i in sorted(set(lines_in_master_dict)))


# DELETE THE FOLDERS/FILES CREATED FOR INTERMEDIATE PROCESSING
path = 'temp_dict_bangla_ortho_new.dict'
if os.path.exists(path):
    os.remove(path)  # delete, if exists

folders_to_remove = ['temp', 'temp_folder_mfa_input', 'temp_output_tgs']
for path in folders_to_remove:
    if os.path.exists(path):
        shutil.rmtree(path)  # delete, if exists

print('All done! Aligned textgrids are saved in "Z_final_aligned_tgs"')
print('')


