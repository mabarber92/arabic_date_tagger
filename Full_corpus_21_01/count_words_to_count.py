# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 11:18:41 2021

@author: mathe
"""

import re

def count (string):
    normal = re.sub(r"\[|\]|\n|ms\d+|[.#|,)():?؟،-]", " ", string)
    count = len(re.findall(r"\s\w+(?=\s)", normal))
    return count

file = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/words_to_count"

with open(file, encoding = "utf-8") as f:
    count = count(f.read())
    f.close()
    
print(count)
    