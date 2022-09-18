#from my_functions import *

filename = '../input_audio_and_transcription_tgs/bangla_news_01.TextGrid'
with open(filename, 'r', encoding='UTF-8')as fr:
    # read in the lines in the file
    text_lines = fr.readlines()
    for line in text_lines:
        print(line)
        # tokens = tokenize_to_words(line)
        # print(tokens)


