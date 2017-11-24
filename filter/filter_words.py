# -*- coding:utf-8 -*-
import string
import re

def in_filtered_words(str):
    new_str = str[:]
    with open('filtered_word.txt', 'r') as f:
        for line in f:
            remove = re.search(line.strip(), str)
            if remove:
                new_str = new_str[:remove.start()] + '**'+new_str[remove.end():]
    return new_str


loop = True
while loop:
    str = raw_input()
    print in_filtered_words(str)
    if str == 'q':
        loop = False
