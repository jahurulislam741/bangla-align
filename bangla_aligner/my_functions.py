import os

#  FUNCTION-1: Tokenize into sentences
def tokenize_to_sents(lines_in_text):  # lines_in_text = fr.readlines(); my_function
    collapsed_string = ''.join(lines_in_text)
    exclude = ['', '.', '~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}',
               '[', ']', '<', '>', '/', ':', ';', '"']
    collapsed_string = ''.join([c for c in collapsed_string if c not in exclude])
    collapsed_string = collapsed_string.replace('\n',' ')  # replace newline characters with spaces
    collapsed_string = collapsed_string.replace('?',' SB')  # replace newline characters with spaces
    collapsed_string = collapsed_string.replace('!',' SB')  # replace newline characters with spaces
    collapsed_string = collapsed_string.replace('।',' SB')  # replace newline characters with spaces
    sents = collapsed_string.split('SB')  # split at the sentence boundary
    sents_list = []
    for s in sents:
        if s != ' ':
            sents_list.append(s)
    return (sents_list)


#  FUNCTION-2: Tokenize into words
def tokenize_to_words(lines_in_text):  # lines_in_text = fr.readlines(); my_function
    with open('files_required_for_scripts/inputFiles/chars_to_exclude.txt', 'r', encoding='UTF-8') as fr:
        lines_in_file = fr.readlines()
        chars_to_exclude = []
        for line in lines_in_file:
            chars_to_exclude.append(line[:-1])  # ':-1' to string the '\n' char
    words_list = []
    sents_list = tokenize_to_sents(lines_in_text)
    for sent in sents_list:
        sent = "".join(c for c in sent if c not in chars_to_exclude) # remove the unwanted characters (e.g. punctuations); see 'files_required_for_scripts/inputFiles/chars_to_exclude.txt'
        words_in_sent = sent.split(' ')
        for word in words_in_sent:
            if word != '':
                words_list.append(word)
    return (words_list)



#  FUNCTION-3: Test if a char is a consonant
def is_consonant(char):
    list_of_consonants = ['ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট', 'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ',
                          'ধ',
                          'ন', 'প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়', 'ঢ়', 'য়', 'ং', 'ঃ']
    if char in list_of_consonants:
        return True
    else:
        return False


#  FUNCTION-4: Test if a char is a vowel
def is_vowel(char):
    list_of_vowels = ['অ', 'আ', 'া', 'ই', 'ি', 'ঈ', 'ী', 'উ', 'ু', 'ঊ', 'ূ', 'এ', 'ে', 'ঐ', 'ৈ', 'ও', 'ো', 'ঔ',
                      'ৌ', '@']
    if char in list_of_vowels:
        return True
    else:
        return False

# CONSONANT CLUSTER MAPPING IN WORDS
'''in bangla some consonants sounds different in different contexts; this function maps them to correct sounds. 
 INPUT file is a txt file with one bangla word in single line. OUTPUT is the list of bangla words with correct mapping.'''

def map_consonants(list_of_words):
    # import the input file containing list of clusters and mapping correspondences
    with open('files_required_for_scripts/inputFiles/exceptional_consonant_mapping.txt', 'r', encoding='UTF-8') as fr:
        list_of_consonant_clusters = fr.readlines()

    # process the out of voc words
    lines_output_file = []  # initiate output file
    # iterate through each word
    for word in list_of_words:
        new_word = word
        # cluster mapping: step 1 (exceptional cons mapping and a letter has a different pronunciation)
        # iterate through each mapping consonant cluster
        for cluster in list_of_consonant_clusters[1:]:  # first line containing comments is excluded
            x = cluster.split(';')  # to remove commented part in each line
            y = x[0].split('=')  # see 'exceptional_consonant_mapping.txt' for more info
            if y[0] in word:  # if the cluster is in the word
                if len(
                        y) > 2:  # when a cluster has two pronunciations. See 'exceptional_consonant_mapping.txt' for more info
                    if word.startswith(y[0]):  # word-initial environment
                        new_word = new_word.replace(y[0], y[1])
                    elif word.endswith(y[0]):  # word-final environment
                        new_word = new_word.replace(y[0], y[2])
                    else:  # word-medial environment
                        new_word = new_word.replace(y[0], y[2])
                else:  # when there is single pronunciation
                    new_word = new_word.replace(y[0], y[1])
        # cluster mapping: step 3 (J-FOLA RULES)
        j_fola = '্' + 'য'
        JH = 'য'
        HOSHONTO = '্'
        CHANDRA_BINDU = 'ঁ'
        if j_fola in new_word:  # find word containing J-fola
            new_string = ''
            for i, char in enumerate(new_word):
                c = char
                if (new_word[1] == HOSHONTO and new_word[2] == JH) or (
                            new_word[1] == CHANDRA_BINDU and new_word[2] == HOSHONTO and new_word[
                    3] == JH):  # word-initial cases
                    if char == HOSHONTO:
                        c = ''
                    elif char == JH:
                        c = '@'
                    elif char == 'া' and i == 3:
                        c = ''
                elif char == JH and i != 2 and new_word[
                    -2] != 'র':  # word-medial and final cases; 3rd 'and' is to exclude কার্যকর
                    if new_word[i - 1] == HOSHONTO:
                        c = new_word[i - 2]
                new_string = new_string + c
            new_word = new_string
        # RI-kar and RI mapping
        if 'ৃ' in new_word:
            new_word = new_word.replace('ৃ', 'রই')
        elif 'ঋ' in new_word:
            new_word = new_word.replace('ঋ', 'রই')
        result = word + ',' + new_word
        lines_output_file.append(result)  # append result to output file
    return lines_output_file


# VOWEL MAPPING IN BANGLA WORDS
'''in bangla some vowels sounds different in different contexts; this function maps them to correct sounds. 
 INPUT file is a txt file with one bangla word in single line. OUTPUT is the list of bangla words with correct mapping.'''
def map_vowels(list_of_words):
    # create list of vowels from external file
    with open('files_required_for_scripts/inputFiles/list_of_vowels.txt', 'r', encoding='UTF-8') as fr:
        vowels_list = fr.readlines()
        Vow = ''
        for v in vowels_list:
            Vow = Vow + v[:-1]
    # create list of consonants from external file
    with open('files_required_for_scripts/inputFiles/list_of_consonants.txt', 'r', encoding='UTF-8') as fr:
        consonant_list = fr.readlines()
        Cons = ''
        for c in consonant_list[1:]:
            Cons = Cons + c[:-1]

    # create list of different CC word types from external files: See source txt files for more info
    with open('files_required_for_scripts/Exception_types/CC_type1.txt', 'r', encoding='UTF-8') as fr:
        CC_words = fr.readlines()
        CC_type1 = []
        for C in CC_words[1:]:
            CC_type1.append(C[:-1])

    # create list of different CCC word types from external files: See source txt files for more info
    with open('files_required_for_scripts/Exception_types/CCC_type1.txt', 'r', encoding='UTF-8') as fr:
        CCC_words = fr.readlines()
        CCC_type1 = []
        for C in CCC_words[1:]:
            CCC_type1.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCC_type2.txt', 'r', encoding='UTF-8') as fr:
        CCC_words = fr.readlines()
        CCC_type2 = []
        for C in CCC_words[1:]:
            CCC_type2.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCC_type3.txt', 'r', encoding='UTF-8') as fr:
        CCC_words = fr.readlines()
        CCC_type3 = []
        for C in CCC_words[1:]:
            CCC_type3.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCC_type4.txt', 'r', encoding='UTF-8') as fr:
        CCC_words = fr.readlines()
        CCC_type4 = []
        for C in CCC_words[1:]:
            CCC_type4.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCC_type5.txt', 'r', encoding='UTF-8') as fr:
        CCC_words = fr.readlines()
        CCC_type5 = []
        for C in CCC_words[1:]:
            CCC_type5.append(C[:-1])

    # create list of different CCCC word types from external files: See source txt files for more info
    with open('files_required_for_scripts/Exception_types/CCCC_type1.txt', 'r', encoding='UTF-8') as fr:
        CCCC_words = fr.readlines()
        CCCC_type1 = []
        for C in CCCC_words[1:]:
            CCCC_type1.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCCC_type2.txt', 'r', encoding='UTF-8') as fr:
        CCCC_words = fr.readlines()
        CCCC_type2 = []
        for C in CCCC_words[1:]:
            CCCC_type2.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCCC_type3.txt', 'r', encoding='UTF-8') as fr:
        CCCC_words = fr.readlines()
        CCCC_type3 = []
        for C in CCCC_words[1:]:
            CCCC_type3.append(C[:-1])
    with open('files_required_for_scripts/Exception_types/CCCC_type4.txt', 'r', encoding='UTF-8') as fr:
        CCCC_words = fr.readlines()
        CCCC_type4 = []
        for C in CCCC_words[1:]:
            CCCC_type4.append(C[:-1])

    # create list of different CCCCC (and more) word types from external files: See source txt files for more info
    with open('files_required_for_scripts/Exception_types/CCCCC_n_plus_manual_mapping.txt', 'r', encoding='UTF-8') as fr:
        CCCCC_n_plus_words = fr.readlines()
        CCCCC_n_plus_phoneme_pairs = []
        for C in CCCCC_n_plus_words[1:]:
            x = C[:-1].split('=')
            result = [x[0], x[1]]
            CCCCC_n_plus_phoneme_pairs.append(result)

    # create list of different AO_initial exceptions from external files: See source txt files for more info
    with open('files_required_for_scripts/Exception_types/AO_initial_exceptions1.txt', 'r', encoding='UTF-8') as fr:
        AO_initial_entries = fr.readlines()
        AO_initial_exceptions1 = []
        for str in AO_initial_entries[1:]:
            AO_initial_exceptions1.append(str[:-1])

    # create list of different EH_initial exceptions from external files: See source txt files for more info
    with open('files_required_for_scripts/Exception_types/EH_initial_exceptions1.txt', 'r', encoding='UTF-8') as fr:
        EH_initial_entries = fr.readlines()
        EH_initial_exceptions1 = []
        for str in EH_initial_entries[1:]:
            EH_initial_exceptions1.append(str[:-1])

    # create list of VCC word types with different pronunciation patterns
    with open('files_required_for_scripts/Exception_types/VCC_type1.txt', 'r', encoding='UTF-8') as fr:
        VCC_words = fr.readlines()
        VCC_type1 = []
        for str in VCC_words[1:]:
            VCC_type1.append(str[:-1])
    with open('files_required_for_scripts/Exception_types/VCC_type2.txt', 'r', encoding='UTF-8') as fr:
        VCC_words = fr.readlines()
        VCC_type2 = []
        for str in VCC_words[1:]:
            VCC_type2.append(str[:-1])
    with open('files_required_for_scripts/Exception_types/VCC_type3.txt', 'r', encoding='UTF-8') as fr:
        VCC_words = fr.readlines()
        VCC_type3 = []
        for str in VCC_words[1:]:
            VCC_type3.append(str[:-1])

    # create list of CVCC word types with different pronunciation patterns
    with open('files_required_for_scripts/Exception_types/CVCC_type1.txt', 'r', encoding='UTF-8') as fr:
        CVCC_words = fr.readlines()
        CVCC_type1 = []
        for str in CVCC_words[1:]:
            CVCC_type1.append(str[:-1])

    # MAIN PROCESSING
    lines_output_file = []  # initiate output file

    HOSHONTO = '্'
    # iterate through each word
    for item in list_of_words:
        raw_word = item.split(',')[0]  # this is the grapheme form as we write
        new_word = item.split(',')[1]  # this is the processed grapheme
        # INSERT VOWEL IN CONSONANT-ONLY WORDS WITHOUT ANY HOSHONTO IN THEM
        if set(new_word).issubset(Cons):  # pick consonant-only words (HOSHONTO not considered as a consonant)
            #  CC WORDS (no hoshonto)
            if len(new_word) == 2:  # when word == CC (2 consonants only)
                if new_word in CC_type1:
                    new_word = new_word[0] + 'অ' + new_word[1] + 'ও'
                else:
                    new_word = new_word[0] + 'অ' + new_word[1]
            # CCC WORDS (no hoshonto)
            elif len(new_word) == 3:  # when word == CCC (3 consonants only)
                if new_word in CCC_type1:
                    new_word = new_word[0] + 'ও' + new_word[1] + new_word[2] + 'ও'
                elif new_word in CCC_type2:
                    new_word = new_word[0] + 'অ' + new_word[1] + 'অ' + new_word[2]
                elif new_word in CCC_type3:
                    new_word = new_word[0] + 'অ' + new_word[1] + new_word[2] + 'ও'
                elif new_word in CCC_type4:
                    new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[2]
                else:
                    new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[2]  # default/elsewhere rule
            # CCCC WORDS (no hoshonto)
            elif len(new_word) == 4:  # when word == CCCC (4 consonants only)
                if new_word in CCCC_type1:  # C AO C OO C AO C
                    new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[2] + 'অ' + new_word[3]
                elif new_word in CCCC_type2:  # C AO C C AO C OO
                    new_word = new_word[0] + 'অ' + new_word[1] + new_word[2] + 'অ' + new_word[3] + 'ও'
                elif new_word in CCCC_type3:  # C AO C C OO C
                    new_word = new_word[0] + 'অ' + new_word[1] + new_word[2] + 'ও' + new_word[3]
                elif new_word in CCCC_type4:  # C AO C OO C AO C OO
                    new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[2] + 'অ' + new_word[3] + 'ও'
                else:  # C AO C C AO C # CCCC_type0_default.txt
                    new_word = new_word[0] + 'অ' + new_word[1] + new_word[2] + 'অ' + new_word[
                        3]  # default/elsewhere rule
            # #  CCCCC-or-more WORDS (no hoshonto)
            elif len(new_word) >= 5:  # when word == CCCCC (5 consonants or more)
                for w in CCCCC_n_plus_phoneme_pairs:  # this is manual phoneme mapping from the list in CCCCC_n_plus_manual_mapping.txt
                    if new_word == w[0]:
                        new_word = w[1]
        # OTHER THAN CONSONANT-ONLY WORDS
        elif not set(new_word).issubset(Cons):  # pick other than consonant-only words
            # word-initial 'অ'
            if new_word[0] == 'অ' and len(new_word) > 1:
                if new_word[
                    1] == '@':  # AO followed by @ (which was mapped for J-fola in 'exceptional_consonant_mapping.py') together becomes AE
                    new_word = new_word[1:]
                if new_word[0] == 'অ' and len(new_word) == 3:
                    if new_word[2] in 'ি  ী  ু  ূ   ':  # AO-->OO
                        new_word = 'ও' + new_word[1:]
                if new_word.startswith(('অতি', 'অভি', 'অতী', 'অনু', 'অরু', 'অধি')):  # AO --> OO for these prefixes
                    new_word = 'ও' + new_word[1:]
                if new_word[0] == 'অ' and len(new_word) >= 4:
                    for AO_str in AO_initial_exceptions1:
                        if new_word.startswith(AO_str):
                            new_word = 'ও' + new_word[1:]  # AO--> if the word begins with the listed strings

            # word-inital 'এ'
            elif new_word[0] == 'এ' and len(new_word) > 1:
                if new_word[
                    1] == '@':  # EH followed by @ ( which was mapped for J-fola in 'exceptional_consonant_mapping.py') together becomes AE
                    new_word = new_word[1:]
                if new_word[0] == 'এ' and len(new_word) > 1:
                    for EH_str in EH_initial_exceptions1:
                        if new_word.startswith(EH_str):
                            new_word = '@' + new_word[1:]

            # other words with both vowels and consonants
            else:
                if len(new_word) == 2:
                    if new_word[0] in Cons:
                        if new_word[1] == 'ই':
                            new_word = new_word[0] + 'ও' + new_word[1]
                        elif new_word[1] == 'ও':
                            new_word = new_word[0] + 'অ' + new_word[1]
                        elif new_word[1] == 'উ':
                            new_word = new_word[0] + 'ও' + new_word[1]

                elif len(new_word) == 3:  # 3 letter/char words
                    if new_word[0] in Vow:  # when vowel-initial
                        if (new_word[1] in Cons) and (new_word[2] in Cons):
                            if new_word in VCC_type1:  # V C C OO
                                new_word = new_word[0:2] + new_word[2] + 'ও'
                            elif new_word in VCC_type2:  # V C AO C OO
                                new_word = new_word[0:2] + 'অ' + new_word[2] + 'ও'
                            elif new_word in VCC_type3:  # V C AO C
                                new_word = new_word[0:2] + 'অ' + new_word[2]
                            else:  # V C OO C
                                new_word = new_word[0:2] + 'ও' + new_word[2]
                    else:  # when consonant initial
                        if (new_word[1] in Cons) and (new_word[2] in 'ি  ী  ু  ূ   '):  # insert OO
                            new_word = new_word[0] + 'ও' + new_word[1:]
                        elif (new_word[1] in Cons) and (new_word[2] not in 'ি  ী  ু  ূ   '):  # insert AO
                            new_word = new_word[0] + 'অ' + new_word[
                                                           1:]  # some verbs need multiple pronunciation (to be manually added, e.g. বসে can be B AO SH EH or B OO SH EH)
                elif len(new_word) == 4:  # 4 letter/char words
                    for i in range(len(new_word) - 1):
                        if (new_word[i] in Cons) and (
                            new_word[i + 1] in Cons):  # finds words with adjacent consonants
                            if HOSHONTO not in new_word:  # b/c HOSHONTO-words hv different rule below in "elif" section
                                if (new_word[0] in Cons) and (new_word[1] in Cons) and (new_word[2] in Vow) and (
                                    new_word[3] in Cons):
                                    if (new_word[2] in 'ি  ী  ু  ূ   ') or (
                                    new_word.endswith(('েছ', 'তেন', 'লাম', 'লেন', 'তাম'))):  # C OO C V C
                                        new_word = new_word[0] + 'ও' + new_word[1:]
                                    else:  # C AO C V C
                                        new_word = new_word[0] + 'অ' + new_word[1:]
                                elif (new_word[0] in Vow) and (new_word[1] in Vow) and (new_word[2] in Cons) and (
                                    new_word[3] in Cons):  # V V C AO C
                                    new_word = new_word[:3] + 'অ' + new_word[3]
                                elif (new_word[0] in Cons) and (new_word[1] in Vow) and (new_word[2] in Cons) and (
                                    new_word[3] in Cons):  # C V C OO C
                                    if new_word[2] in 'ং, ঙ, ঃ':  # C V C C OO e.g. মাংস
                                        new_word = new_word + 'ও'
                                    elif new_word in CVCC_type1:  # C V C C OO e.g. আনব
                                        new_word = new_word + 'ও'
                                    else:  # C V C OO C e.g. আসল
                                        new_word = new_word = new_word[:3] + 'ও' + new_word[3]
                            elif HOSHONTO in new_word:
                                if new_word[2] == HOSHONTO:
                                    new_word = new_word + 'ও'
                                elif new_word[1] == HOSHONTO:
                                    new_word = new_word[:3] + 'অ' + new_word[3]

                elif len(new_word) == 5:  # 5 letter/char words
                    for i in range(len(new_word) - 1):
                        if (new_word[i] in Cons) and (
                            new_word[i + 1] in Cons):  # finds words with 2 adjacent consonants
                            if HOSHONTO not in new_word:  #
                                if (new_word[len(new_word) - 1] in Cons) and (new_word[len(
                                        new_word) - 2] in Cons):  # if ends with 2 Cons, insert AO between them
                                    new_word = new_word[:len(new_word) - 1] + 'অ' + new_word[len(new_word) - 1]
                                else:
                                    for i in range(len(new_word) - 3):
                                        if (new_word[i] in Cons) and (new_word[i + 1] in Cons) and (
                                            new_word[i + 2] in Cons) and (
                                            new_word[i + 3] in Cons):  # finds words with 3 adjacent consonants
                                            if new_word.endswith(('কে', 'টা', 'টি')):
                                                new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[2:]
                                            else:
                                                if new_word[1] == 'ং':
                                                    new_word = new_word[0] + 'অ' + new_word[1:3] + 'ও' + new_word[
                                                                                                         3:]
                                                elif new_word[1] == new_word[3]:
                                                    new_word = new_word[0] + 'অ' + new_word[1:3] + 'অ' + new_word[
                                                                                                         3:]
                                                else:
                                                    new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[
                                                        2] + 'অ' + new_word[3:]
                            else:
                                if new_word[1] == HOSHONTO:  # গ্রহণ
                                    new_word = new_word[:3] + 'ও' + new_word[3:]
                                    if new_word[5] not in Vow:
                                        new_word = new_word[:5] + 'ও' + new_word[5]
                                elif new_word[2] == HOSHONTO:  # e.g. সত্তা
                                    if new_word[4] in Cons:  # e.g. সপ্তম
                                        new_word = new_word[:4] + 'ও' + new_word[4]
                                    else:
                                        if new_word[4] in Vow:  # শক্তি
                                            if new_word[4] in 'ি  ী  ু  ূ   ':  # বস্তি
                                                new_word = new_word[0] + 'ও' + new_word[1:]
                                            else:  # সস্তা
                                                new_word = new_word[0] + 'অ' + new_word[1:]
                                elif new_word[3] == HOSHONTO:  # e.g.
                                    if new_word[0] in Cons:  # তদন্ত
                                        new_word = new_word[0] + 'অ' + new_word[1] + 'ও' + new_word[2:] + 'ও'
                                    else:  # আনন্দ
                                        new_word = new_word[:2] + 'ও' + new_word[2:] + 'ও'
                elif len(new_word) == 6:
                    if HOSHONTO in new_word:
                        word_split = new_word.split(HOSHONTO)
                        word_rejoined = ""
                        for i, word_part in enumerate(word_split):
                            if i != len(word_split) - 1:  # when the word part is NOT the final one
                                if len(word_part) == 2 and set(word_part).issubset(Cons):
                                    word_part = word_part[0] + 'অ' + word_part[1]
                                elif len(word_part) == 3 and set(word_part).issubset(Cons):
                                    if word_part[1] == "ং":
                                        word_part = word_part[0] + 'অ' + word_part[1:]
                                    else:
                                        word_part = word_part[0] + 'অ' + word_part[1] + 'ও' + word_part[2:]
                                elif len(word_part) > 3 and set(word_part).issubset(Cons):
                                    word_part = word_part[0] + 'অ' + word_part[1] + 'ও' + word_part[
                                        2] + 'অ' + word_part[3:]
                            # add 'ও' to the end of the word
                            elif i == len(word_split) - 1 and len(word_part) == 1 and set(word_part).issubset(
                                    Cons):  # when the word part IS the final one with a single consonant
                                word_part = word_part + 'ও'
                            # rejoin the word parts
                            word_rejoined = word_rejoined + word_part
                        new_word = word_rejoined

        result = raw_word + ',' + new_word
        lines_output_file.append(result)
    return lines_output_file



# BANGLA GRAPHEME TO PHONEME MAPPING
'''transliterates bangla words into english orthography, and provides the list of phonemes for each bangla word '''
def map_grapheme_to_phoneme(list_of_words):
    # BANGLA GRAPHEME TO PHONEME MAPPING
    # make a list of mapping correspondence from external file
    with open('files_required_for_scripts/inputFiles/grapheme2phoneme_mapping.txt', 'r', encoding='UTF-8') as fr:
        lines_in_file = fr.readlines()
        mapping_list = []
        for line in lines_in_file:
            mapping_list.append(line[:-1])  # ':-1' to remove the '\n' char

    # import the data in source encoding (bangla font)
    lines_output_file = []  # initiate an output file
    # transliterate each word (one in each line) at letter level (this is not PHONEME mapping)
    for line_string in list_of_words:
        wordInBanglaFont = line_string.split(",")[0]  # this is the word as used in written Bangla font
        wordInPhoneme = line_string.split(",")[1]  # this is the phoneme mapped word in Bangla font
        wordInEnglishFont = line_string.split(",")[0]  # at this point, it is in Bangla font, to be transliterated below
        # loop through each mapping pairs in the mapping list (generated above)
        for item in mapping_list[:-1]:  # ':-1' to remove last line which usually not giving the [2]th char
            x = item.split(' ')
            wordInEnglishFont = wordInEnglishFont.replace(x[0], x[2])  # replace/map the char
        wordInEnglishFont = wordInEnglishFont.replace("'", "")

        # TRANSLITERATE INTO PHONEMES
        # loop through each mapping pairs in the mapping list (generated above)
        phonemes = ''
        for char in wordInPhoneme:
            for item in mapping_list[:-1]:  # ':-1' to remove last line which usually not giving the [2]th char
                x = item.split(' ')
                if char == x[0]:
                    new_char = x[1]
                    phonemes = phonemes + ' ' + new_char
        # remove "'" apostrophe (representing HOSHONTO character) from word
        phonemes = phonemes.replace(" '", "")
        #result = wordInBanglaFont + '   ' + wordInEnglishFont + '   ' + phonemes[1:]
        result = wordInBanglaFont + '   ' + phonemes[1:]
        lines_output_file.append(result)
    return lines_output_file


# THIS FUNCTION EXTRACTS THE WORDS FROM A TEXTGRID AND RETURN A LIST
''' input is a list of the lines in a textgrid file; output in the list of words'''
def list_words_from_texgrid(lines_in_file):
    word_list = []
    for line in lines_in_file:
        if 'text' in line:
            x = line.split('"')
            y = " ".join(x[1].split())
            for i in tokenize_to_words(y):
                word_list.append(i)
    return word_list
    # print(word_list)


# TRANSLITERATE BANGLA ORTHOGRAPHY IN TEXTGRID INTO ENGLISH
''' input = lines_in_a_textgrid; output = list_of_modified_lines to be writted as a new TextGrid file'''
def transliterate_TG_to_eng_ortho(lines_in_texgrid):
    with open('files_required_for_scripts/master_phoneme_dictionary.txt', 'r', encoding='UTF-8')as fr:
        # read in the lines in the file
        words_in_master_dict = []
        text_lines_in_dict = fr.readlines()
        # add entries from oov file, if exists
        oov_file = 'oov_with_phoneme_suggestions.txt'
        if os.path.isfile(oov_file):
            with open(oov_file, 'r', encoding='UTF-8')as fr:
                lines_in_oov_file = fr.readlines()
                for l in lines_in_oov_file:
                    text_lines_in_dict.append(l)

        for line in text_lines_in_dict[1:]:
            x = line[:-1].split('   ')
            words_in_master_dict.append(x[0])

    new_lines = []
    for line in lines_in_texgrid:
        if 'text' not in line:
            new_lines.append(line)
        elif 'text' in line:
            x = line.split('"')
            if len(x[1]) == 0:  # for empty intervals
                new_lines.append(line)
            else:
                text_string = " ".join(x[1].split())
                words = tokenize_to_words(text_string)
                output_interval_text = ''
                for word in words:
                    # if word in words_in_master_dict:
                    index = words_in_master_dict.index(word)  # find word's index in master dictionary
                    new_value = text_lines_in_dict[index + 1].split('   ')[1]  # get the english orthography
                    output_interval_text = output_interval_text + new_value + ' '
                output_line = 'text = "' + output_interval_text + '"' + '\n'
                new_lines.append(output_line)
    return new_lines



# TRANSLITERATE ENGLISH ORTHOGRAPHY IN TEXTGRID INTO BANGLA
''' input = lines_in_a_textgrid; output = list_of_modified_lines to be writted as a new TextGrid file'''
def transliterate_TG_to_bang_ortho(lines_in_texgrid):
    # create a list of words in master_phoneme_dict
    with open('dictionary_generator/temp_master_phoneme_dict.dict', 'r', encoding='UTF-8')as fr: # the input file must be in the same directory as my_functions.py
        # read in the lines in the file
        words_in_master_dict = []
        text_lines_in_dict = fr.readlines()
        for line in text_lines_in_dict[1:]:
            x = line[:-1].split('   ')
            words_in_master_dict.append(x[1])

    # process the lines in the textgrid file
    new_lines = []
    tier_2_start_id = lines_in_texgrid.index('\titem [2]:\n') # get the point before which word tier ends
    for line in lines_in_texgrid:
        if 'text' not in line: # nothing to change when this is not the line containing word labels
            new_lines.append(line)
        elif 'text' in line:
            if lines_in_texgrid.index(line) < tier_2_start_id: # if the line is inside the word tier
                x = line.split('"')
                word = x[1]
                if len(x[1]) == 0:  # for empty intervals
                    new_lines.append(line)
                else:
                    index = words_in_master_dict.index(word.upper())  # find word's index in master dictionary
                    new_value = text_lines_in_dict[index + 1].split('   ')[0]  # get the english orthography
                    output_line = 'text = "' + new_value + '"' + '\n'
                    new_lines.append(output_line)
            else:
                new_lines.append(line) # add lines after the word ending point as they are
        # else:
        #     new_lines.append(line)
    return new_lines
	

#### THIS FUNCTION ADDS 'X' in WORD-final position
#### WORKS ON A WHOLE TEXTGRID FILE AT A TIME
def add_X_word_finally_in_TGs(lines_in_texgrid):
    new_lines = []
    for line in lines_in_texgrid:
        if 'text' not in line:
            new_lines.append(line)
        elif 'text' in line:
            x = line.split('"')
            if len(x[1]) == 0:  # for empty intervals
                new_lines.append(line)
            else:
                text_string = " ".join(x[1].split())
                words = tokenize_to_words(text_string)
                output_interval_text = ''
                for word in words:
                    # replace word-final diacrtic
                    word = word + 'x'
                    output_interval_text = output_interval_text + ' ' + word
                output_line = 'text = "' + output_interval_text + '"' + '\n'
                new_lines.append(output_line)
    return new_lines


#### THIS FUNCTION removes 'X' from the WORD-final position
#### WORKS ON A WHOLE TEXTGRID FILE AT A TIME
def remove_word_final_X_in_TGs(lines_in_texgrid):
    new_lines = []
    for line in lines_in_texgrid:
        if 'text' not in line:
            new_lines.append(line)
        elif 'text' in line:
            x = line.split('"')
            if len(x[1]) == 0:  # for empty intervals
                new_lines.append(line)
            else:
                text_string = " ".join(x[1].split())
                words = tokenize_to_words(text_string)
                output_interval_text = ''
                for word in words:
                    # replace word-final diacrtic
                    word = word[:-1]
                    output_interval_text = output_interval_text + ' ' + word
                output_line = 'text = "' + output_interval_text + '"' + '\n'
                new_lines.append(output_line)
    return new_lines
