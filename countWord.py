import string
import re
from collections import Counter


def count_words():
    with open('doc.txt', 'r') as f:
        doc = f.read()
        print doc
    pattern = '[a-zA-Z-]+'
    words = re.findall(pattern, doc)
    print Counter(words).items()

count_words()