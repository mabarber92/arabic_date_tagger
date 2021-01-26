# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:34:52 2021

@author: mathe
"""
import re

def md_seg (text, md_level):
    md_str = "###\s"
    end_md_str = "###\s"
    
    for x in range(0, md_level):
        md_str = md_str + "\|"
        
    if md_level > 1:
        for x in range(0, md_level):
            end_md_str = end_md_str + "\|?"
    else:
        end_md_str = md_str
    
    regex = "(" + md_str + "\s(.*\n)+?)" + "(?="+end_md_str + "\s)"
    
    split_text = ["".join(x) for x in re.findall(regex, text)]
    return split_text

test = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/teszt/test_doc"

with open(test, encoding = "utf-8") as f:
                # Adding final markdown marker to allow markdown segmenter to locate all segments
                whole_text = f.read() + "\n### | "
                first_split = md_seg(whole_text, 2)
                f.close()

for item in first_split:
    md_header = re.findall(r"(###.+\n)", item)
    print(md_header)
