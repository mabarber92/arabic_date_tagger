# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 12:17:26 2020

@author: mathe
"""


import pandas as pd
import re
import os
import copy

# Functions for working with the md

def md_seg (text, md_level):
    md_str = "###\s"
    for x in range(0, md_level):
        md_str = md_str + "\|"
    regex = "(" + md_str + "\s(.*\n)+?)" + "(?="+md_str + "\s)"
    split_text = ["".join(x) for x in re.findall(regex, text)]
    return split_text

def count (string):
    normal = re.sub(r"\[|\]|\n|ms\d+|[.#|,)():?؟،-]", " ", string)
    count = len(re.findall(r"\s\w+(?=\s)", normal))
    return count

def md_leveler (text):
    md_levels = re.findall(r"###\s(\|+)\s", text)
    levels_no = []
    for level in md_levels:
        levels_no.append(len(level))
    maxi = max(levels_no)
    return maxi 


# Functions for working with the dates

def line_y_tag (line, csv):
        
        dates_1 = csv[["1s", "1_no"]].dropna().values.tolist()
        dates_10 = csv[["10s", "10s_no"]].dropna().values.tolist()
        dates_100 = csv[["100s", "100s_no"]].dropna().values.tolist()
        dates_100_sep = csv[["100_1","100_1_no"]].dropna().values.tolist()
        start_terms = csv[["year", "meaning"]].dropna().values.tolist()
        exc_100 = "مائة"
        exc_100_2 = "مئة"
    
        line_build = []
        
        date_build = []
        line_build.append(line)
        y_type = False
        year_2 = False
        num = False
        y_type_2 = False
        line_clean = re.sub(r"ms\d+|\]|\[|\d+|[,./؟\?!()«»،:]|###|\|", "", line)    
        line_split = line_clean.split()
        n_tok = len(line_split) - 1
        d1 = "0"
        d2 = "0"
        d3 = "0"
        d1_2 = "0"
        d2_2 = "0"
        d3_2 = "0"
        tho = False
        
        # Checking for thousands
        if re.search(r"\bو?[اأ]لف\b", line_clean):
            tho = True
        
        # Checking for numerals - very basic - no advanced functions
        
        if re.search(r"ا?[ال]?سنة\s\d{3}", line):
            year_n = re.findall(r'ا?[ال]?سنة\s(\d{3})', line)[0].split()
            
            y_type = 'year'
            num = True
        
        for idx, tok in enumerate(line_split):
                if num:
                    break
                for term in start_terms:
                    if year_2:
                        break
                    if tho:
                        break
                    if re.search(term[0], tok):
                        pos_1 = idx+1
                        pos_2 = idx+2
                        pos_3 = idx+3
                        pos_4 = idx+4
                        pos_5 = idx+5
                        
                        rem_tok = n_tok - idx
                        y_type = term[1]
                                                
                        # Finding 3 word numbers
                        if rem_tok >= 3:
                            years = re.findall("\bو?سن[هة]|\bو?السنة|\bلسنة", line)
                            # Dealing with cases where 2 years in one line
                            if len(years) == 2:
                                
                                # Recording position of second sana
                                year_pos = []
                                for idx_0, tok_0 in enumerate(line_split):
                                    if re.match("و?سن[هة]|و?السنة|لسنة", tok_0):
                                        year_pos.append(idx_0)
                                
                                
                                for idx_1, tok_2 in enumerate(line_split):
                                    
                                    if year_2:
                                        break
                                    
                                    if tok_2 == years[0]:
                                        pos_1 = idx_1+1
                                        pos_2 = idx_1+2
                                        pos_3 = idx_1+3
                                        pos_4 = idx_1+4
                                        pos_5 = idx_1+5  
                                        y_type_2 = "year"
                                        
                                        
                                        try:
                                        
                                            for digit_1 in dates_1:
                                                if digit_1[0] == line_split[pos_1]:                                                    
                                                    d1 = digit_1[1]
                                                    break
                                            for digit_2 in dates_10:
                                                if digit_2[0] == line_split[pos_2] or digit_2[0] == line_split[pos_1]:                                                
                                                    d2 = digit_2[1]
                                                    break
                                            for digit_3 in dates_100:
                                                if digit_3[0] == line_split[pos_3] or digit_3[0] == line_split[pos_2] or digit_3[0] == line_split[pos_1]:
                                                    d3 = digit_3[1]
                                                    break
                                                    
                                    # Exceptions - split 100s and non-chronicle year types
                                            if line_split[pos_2] == exc_100 or line_split[pos_2] == exc_100_2:
                                                for digit_1 in dates_100_sep:
                                                    if digit_1[0] == line_split[pos_1]:
                                                        
                                                        d3 = digit_1[1]
                                                        d2 = '0'
                                                        d1 = '0'
                                            # Finding cases of 'ba'd miyya'
                                            if line_split[pos_3] == "بعد":                                
                                                        
                                                try:
                                                    if line_split[pos_5] == exc_100 or line_split[pos_5] == exc_100_2:
                                                        for digit_1 in dates_100_sep:
                                                            if digit_1[0] == line_split[pos_4]:
                                                                d3 = digit_1[1]
                                                                break
                                                except IndexError:
                                                    pass                                                        
                                                for digit_3 in dates_100:
                                                    if digit_3[0] == line_split[pos_4]:
                                                        d3 = digit_3[1]
                                                        break
                                            
                                            try:
                                                if line_split[pos_2] == "مولده" or line_split[pos_3] == "مولده" or line_split[pos_4] == "مولده" or line_split[pos_5] == "مولده":
                                                    y_type = 'from_birth'
                                            except IndexError:
                                                pass
                                
                                            if line_split[pos_2] == "من" :
                                                if line_split[pos_3] == "ولاية" or line_split[pos_3] == "سلطنة":
                                                    y_type = "regnal"
                                                if line_split[pos_3] == "مولده" or line_split[pos_3] == "الفيل":
                                                    y_type = "from_birth"
                                                
                                                if line_split[pos_3] == "النبوة" or line_split[pos_3] == "البعثة":
                                                    y_type = "from_prophecy"
                                            if line_split[pos_2] == "ولاية" :
                                                y_type = "regnal"
                                            elif line_split[pos_3] == exc_100 or line_split[pos_3] == exc_100_2:
                                                for digit_1 in dates_100_sep:
                                                    if digit_1[0] == line_split[pos_2]:
                                                        d3 = digit_1[1]
                                        
                                            elif line_split[pos_3] == "من" :
                                        
                                              
                                                if line_split[pos_4] == "ولاية" or line_split[pos_4] == "سلطنة":
                                                    y_type = "regnal"
                                                if line_split[pos_4] == "مولده" or line_split[pos_4] == "الفيل":
                                                    y_type = "from_birth"
                                                
                                                if line_split[pos_4] == "النبوة" or line_split[pos_4] == "البعثة":
                                                    y_type = "from_prophecy"
                                            elif line_split[pos_3] == "ولاية" :
                                                y_type = "regnal"
                                        except IndexError:
                                            pass
                                        try:
                                            if line_split[pos_4] == exc_100 or line_split[pos_4] == exc_100_2:
                                                for digit_1 in dates_100_sep:
                                                    if digit_1[0] == line_split[pos_3]:
                                                        d3 = digit_1[1]
                                                        break
                                # Dropping cases where the year is regnal
                                            elif line_split[pos_4] == "من" :
                                                if line_split[pos_5] == "ولاية" or line_split[pos_5] == "سلطنة":
                                                    y_type = "regnal"
                                                if line_split[pos_5] == "مولده" or line_split[pos_5] == "الفيل":
                                                    y_type = "from_birth"
                                                
                                                if line_split[pos_5] == "النبوة" or line_split[pos_5] == "البعثة":
                                                    y_type = "from_prophecy"
                                            elif line_split[pos_4] == "ولاية" :
                                                y_type = "regnal"
                                    
                                        except IndexError:
                                            pass
                                        rem_split = line_split[slice(year_pos[1], None)]                                        
                                        n_tok_2 = len(rem_split)
                                        
                                        # Second year
                                        for idx_2, tok_2 in enumerate(rem_split):
                                    
                                            if re.search("سنة", tok_2):
                                        
                                                pos_1 = idx_2+1
                                                pos_2 = idx_2+2
                                                pos_3 = idx_2+3
                                                pos_4 = idx_2+4
                                                pos_5 = idx_2+5
                                                rem_tok_2 = n_tok_2 - (idx_2 +1)
                                        
                                        
                                                if rem_tok_2 >= 3:
                                                    
                                                    for digit_1 in dates_1:
                                                        if digit_1[0] == rem_split[pos_1]:
                                                            d1_2 = digit_1[1]
                                                            break
                                                    for digit_2 in dates_10:                                                        
                                                        if digit_2[0] == rem_split[pos_2] or digit_2[0] == rem_split[pos_1]:
                                                            d2_2 = digit_2[1]
                                                            break                                                            
                                                    for digit_3 in dates_100:
                                                        if digit_3[0] == rem_split[pos_3] or digit_3[0] == rem_split[pos_2] or digit_3[0] == rem_split[pos_1]:
                                                            d3_2 = digit_3[1]
                                                            break
                                # Exceptions - split 100s and non-chronicle year types
                                                    if rem_split[pos_2] == exc_100 or rem_split[pos_2] == exc_100_2:
                                                        for digit_1 in dates_100_sep:
                                                            if digit_1[0] == line_split[pos_1]:
                                                                d3_2 = digit_1[1]
                                                                d2_2 = '0'
                                                                d1_2 = '0'
                                                                break
                                                    # Finding cases of 'ba'd miyya'
                                                    if rem_split[pos_3] == "بعد":                                
                                                        
                                                        try:
                                                            if rem_split[pos_5] == exc_100 or rem_split[pos_5] == exc_100_2:
                                                                for digit_1 in dates_100_sep:
                                                                    if digit_1[0] == rem_split[pos_4]:
                                                                        d3_2 = digit_1[1]
                                                                        break
                                                        except IndexError:
                                                            pass                                                        
                                                        for digit_3 in dates_100:
                                                                if digit_3[0] == rem_split[pos_4]:
                                                                    d3_2 = digit_3[1]
                                                    try:
                                                        if rem_split[pos_2] == "مولده" or rem_split[pos_3] == "مولده" or rem_split[pos_4] == "مولده" or rem_split[pos_5] == "مولده":
                                                            y_type = 'from_birth'
                                                    except IndexError:
                                                        pass
                                                    if rem_split[pos_2] == "من" :
                                                        if rem_split[pos_3] == "ولاية" or rem_split[pos_3] == "سلطنة":
                                                            y_type_2 = "regnal"
                                                        if rem_split[pos_3] == "مولده":
                                                            y_type_2 = "from_birth"
                                                    if rem_split[pos_2] == "ولاية" :
                                                        y_type_2 = "regnal"
                                                    elif rem_split[pos_3] == exc_100 or rem_split[pos_3] == exc_100_2:
                                                            for digit_1 in dates_100_sep:
                                                                if digit_1[0] == rem_split[pos_2]:
                                                                    d3_2 = digit_1[1]
                                                    elif rem_split[pos_3] == "من" :
                                                            try:    
                                                                if rem_split[pos_4] == "ولاية" or rem_split[pos_4] == "سلطنة":
                                                                   y_type_2 = "regnal"
                                                                if rem_split[pos_4] == "مولده":
                                                                    y_type_2 = "from_birth"
                                                            except IndexError:
                                                                pass
                                                    elif rem_split[pos_3] == "ولاية" :
                                                        y_type_2 = "regnal"
                                                    try:
                                                        if rem_split[pos_4] == exc_100:
                                                               for digit_1 in dates_100_sep:
                                                                   if digit_1[0] == rem_split[pos_3]:
                                                                       d3_2 = digit_1[1]
                                                                       break
                                # Dropping cases where the year is regnal
                                                        elif rem_split[pos_4] == "من" :
                                                                if rem_split[pos_5] == "ولاية" or rem_split[pos_5] == "سلطنة":
                                                                    y_type_2 = "regnal"
                                                                if rem_split[pos_5] == "مولده":
                                                                    y_type_2 = "from_birth"
                                                        elif rem_split[pos_4] == "ولاية" :
                                                            y_type_2 = "regnal"
                                    
                                                    except IndexError:
                                                        pass

                            

                                                elif rem_tok_2 == 2:
                                                    for digit_1 in dates_1:
                                                        if digit_1[0] == rem_split[pos_1]:
                                                            d1_2 = digit_1[1]
                                                            break
                                                    for digit_2 in dates_10:
                                                        if digit_2[0] == rem_split[pos_2] or digit_2[0] == rem_split[pos_1]:
                                                            d2_2 = digit_2[1]
                                                            break
                                                    for digit_3 in dates_100:
                                                        if digit_3[0] == rem_split[pos_2] or digit_3[0] == rem_split[pos_1]:
                                                            d3_2 = digit_3[1]
                                                            break
                                                    if rem_split[pos_2] == exc_100 or rem_split[pos_2] == exc_100_2:
                                                        for digit_1 in dates_100_sep:
                                                           if digit_1[0] == rem_split[pos_1]:
                                                               d3_2 = digit_1[1]
                                                               d2_2 = '0'
                                                               d1_2 = '0'
                                                               break
                            


                                                elif rem_tok_2 == 1:
                                                    for digit_1 in dates_1:
                                                        if digit_1[0] == rem_split[pos_1]:
                                                            d1_2 = digit_1[1]
                                                            break
                                                    for digit_2 in dates_10:
                                                        if digit_2[0] == rem_split[pos_1]:
                                                            d2_2 = digit_2[1]
                                                            break
                                                    for digit_3 in dates_100:
                                                        if digit_3[0] == rem_split[pos_1]:
                                                            d3_2 = digit_3[1]
                                                            break
                                
                                        
                                        # Resetting year type to range if a signifier of a date range is encountered
                                        if line_split[year_pos[1]-1] == 'الى':
                                            y_type = 'range'
                                            y_type_2 = 'range'
                                        
                                        year_2 = True
                                        
                                       
                                

                            
# Looking for cases of 1 year 
                            else:
                                if d1 != '0' and d2 != '0' and d3 != '0':
                                    break
                                
                                for digit_1 in dates_1:
                                    if digit_1[0] == line_split[pos_1]:
                                        d1 = digit_1[1]
                                        break
                                for digit_2 in dates_10:
                                    if digit_2[0] == line_split[pos_2] or digit_2[0] == line_split[pos_1]:
                                        d2 = digit_2[1]
                                        break
                                for digit_3 in dates_100:
                                    
                                    if digit_3[0] == line_split[pos_3] or digit_3[0] == line_split[pos_2] or digit_3[0] == line_split[pos_1]:
                                        d3 = digit_3[1]
                                        break
                                        
                                if line_split[pos_2] == exc_100 or line_split[pos_2] == exc_100_2:
                                    for digit_1 in dates_100_sep:
                                        if digit_1[0] == line_split[pos_1]:                                            
                                            d3 = digit_1[1]
                                            d2 = '0'
                                            d1 = '0'
                                            break
                                
                                # Finding cases of 'ba'd miyya'
                                if line_split[pos_3] == "بعد":                                
                                                        
                                    try:
                                        if line_split[pos_5] == exc_100 or line_split[pos_5] == exc_100_2:
                                            for digit_1 in dates_100_sep:
                                                if digit_1[0] == line_split[pos_4]:
                                                    d3 = digit_1[1]
                                                    break
                                    except IndexError:
                                        pass                                                        
                                    for digit_3 in dates_100:
                                        if digit_3[0] == line_split[pos_4]:
                                            d3 = digit_3[1]
                                            break
                                
                                # Exceptions - split 100s and non-chronicle year types
                                try:
                                    if line_split[pos_2] == "مولده" or line_split[pos_3] == "مولده" or line_split[pos_4] == "مولده" or line_split[pos_5] == "مولده":
                                        y_type = 'from_birth'
                                except IndexError:
                                    pass
                                if line_split[pos_2] == "من" :
                                    if line_split[pos_3] == "ولاية" or line_split[pos_3] == "سلطنة":
                                        y_type = "regnal"
                                    if line_split[pos_3] == "مولده" or line_split[pos_3] == "الفيل":
                                        y_type = "from_birth"
                                    
                                    if line_split[pos_3] == "النبوة" or line_split[pos_3] == "البعثة":
                                                    y_type = "from_prophecy"
                                    if line_split[pos_3] == "النبوة" or line_split[pos_3] == "البعثة":
                                                    y_type = "from_prophecy"
                                if line_split[pos_2] == "ولاية" :
                                    y_type = "regnal"
                                elif line_split[pos_3] == exc_100 or line_split[pos_3] == exc_100_2:
                                   
                                   for digit_1 in dates_100_sep:
                                       if digit_1[0] == line_split[pos_2]:
                                            d3 = digit_1[1]
                                elif line_split[pos_3] == "من" :
                                    try:    
                                        if line_split[pos_4] == "ولاية" or line_split[pos_4] == "سلطنة":
                                            y_type = "regnal"
                                        if line_split[pos_4] == "مولده" or line_split[pos_4] == "الفيل":
                                            y_type = "from_birth"
                                        
                                        if line_split[pos_4] == "النبوة" or line_split[pos_4] == "البعثة":
                                                    y_type = "from_prophecy"
                                    except IndexError:
                                        pass
                                try:
                                    
                                    if line_split[pos_4] == exc_100 or line_split[pos_4] == exc_100_2:
                                            
                                            for digit_1 in dates_100_sep:
                                                if digit_1[0] == line_split[pos_3]:
                                                    d3 = digit_1[1]
                                # Dropping cases where the year is regnal
                                    elif line_split[pos_4] == "من" :
                                            if line_split[pos_5] == "ولاية" or line_split[pos_5] == "سلطنة":
                                                y_type = "regnal"
                                            if line_split[pos_5] == "مولده" or line_split[pos_5] == "الفيل":
                                                y_type = "from_birth"
                                    
                                except IndexError:
                                    pass
                                if line_split[pos_3] == "ولاية" :
                                    y_type = "regnal"
                                    
                                
                            

                        elif rem_tok == 2:
                            for digit_1 in dates_1:
                                if digit_1[0] == line_split[pos_1]:
                                    d1 = digit_1[1]
                                    break
                            for digit_2 in dates_10:
                                if digit_2[0] == line_split[pos_2] or digit_2[0] == line_split[pos_1]:
                                    d2 = digit_2[1]
                                    break
                            for digit_3 in dates_100:
                                if digit_3[0] == line_split[pos_2] or digit_3[0] == line_split[pos_1]:
                                    d3 = digit_3[1]
                                    break
                            if line_split[pos_2] == exc_100 or line_split[pos_2] == exc_100_2:
                                for digit_1 in dates_100_sep:
                                    if digit_1[0] == line_split[pos_1]:
                                        d3 = digit_1[1]
                                        d2 = '0'
                                        d1 = '0'
                                        break
                            
                            

                        elif rem_tok == 1:
                            for digit_1 in dates_1:
                                if digit_1[0] == line_split[pos_1]:
                                    d1 = digit_1[1]
                                    break
                            for digit_2 in dates_10:
                                if digit_2[0] == line_split[pos_1]:
                                    d2 = digit_2[1]
                                    break
                            for digit_3 in dates_100:
                                if digit_3[0] == line_split[pos_1]:
                                    d3 = digit_3[1]
                                    break

                            
    
         
        date_build = d3 + d2 + d1                
        # Summary match stats
        
        if num:
            date_build = year_n[0]
        
        line_build.append(date_build)
        line_build.append(y_type)
            
            
        
       
        date_build_2 = d3_2 + d2_2 + d1_2
        
        
        line_build.append(date_build_2)
        line_build.append(y_type_2)
       
        return line_build


def cent_loc (date):
    split = list(date)
    return split[0]

def dec_loc (date):
    split = list(date)
    return split[1]

def cent_dec_pred (date, cent, dec):
    split = list(date)
    new_date = date
    if split[0] == "0" and split[1] != "0":
            
        new_date = cent + ''.join(split[1:])

    if split[0] == "0" and split[1] == "0":
        new_date = cent + dec + split[2]

    return new_date

# Create a template for years to be checked against
year_count = 0
full_stats = []
for x in range(0, 999):
    year_count = year_count+1
    y_line = []
    if year_count < 10:
        year = "00" + str(year_count)
    elif year_count < 100:
        year = "0" + str(year_count)
    else:
        year = str(year_count)
    y_line.append(year)
    y_line.append(0)
    y_line.append(0)
    full_stats.append(y_line)

full_stats_pre = copy.deepcopy(full_stats)

metadata = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/kitab-corpusmetadata_25_10.csv")[["Book Id", "Status"]]
pri_list = metadata[metadata.Status == 'pri'].values.tolist()


csv = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Python manipulation scripts/Test dates df.csv", dtype=str)

directory = r"C:/Users/mathe/Documents/Kitab project/25-year repos direct clone"

os.chdir(directory)

error_rep = []


for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pri = False
        if re.search(".*.yml", name):
            continue
        print("Trying: " + name, end =' ..... ')
        try:
            b_id = re.findall(r"\d\d\d\d\w+?\.\w+?\.(\w+|\d+)-ara1", name)[0]
            d_date = re.findall(r"(\d\d\d\d)\w+?\.\w+?\.\w+|\d+-ara1", name)[0]
        except IndexError:
            print('error ')
            rep = []
            rep.append(name)
            rep.append("regex_error")
            error_rep.append(rep)
            continue
        for book in pri_list:
            if book[0] == b_id:
                print('primary')
                pri_list.remove(book)
                pri = True
                break
        if not pri:
            print('secondary')
            continue
        
        if pri:
            
            path_e = os.path.join(root, name)
            path = os.path.abspath(path_e)
            file_name = name            
            neg_c = 0
            neg = False
            pre_date = False

            # Set max level to determine maximum loops for splitting
            try:
                with open(path, encoding = "utf-8") as f:
                    max_l = md_leveler(f.read())
                    f.close()
                    
            except ValueError:
                print("no markdown found")
                continue
            
            # Perform initial split on markdown headings    
            with open(path, encoding = "utf-8") as f:
                # Adding final markdown marker to allow markdown segmenter to locate all segments
                whole_text = f.read() + "\n### | "
                first_split = md_seg(whole_text, 1)
                f.close()

            out = []
            cent = "0"
            dec = "0"
            
            
            
            # Begin creation of text-spec file and summary
            for sect in first_split:
                
                
                # Tag first level
                md_header = re.findall(r"(###.+\n)", sect)
                
                toks = count(sect)
                out_line = line_y_tag(md_header[0], csv)
    
                # Predicting actual dates
                if out_line[2] == "year":
                    cent_tem = cent_loc(out_line[1])
                    dec_tem = dec_loc(out_line[1])
                    if cent_tem != "0":
                        cent = cent_tem
                        dec = dec_tem
                    if cent_tem == "0" and dec_tem != "0":
                        dec = dec_tem
                if out_line[4] == "year":
                    cent_tem = cent_loc(out_line[3])
                    dec_tem = dec_loc(out_line[3])
                    if cent_tem != "0":
                       cent = cent_tem
                       dec = dec_tem
                    if cent_tem == "0" and dec_tem != "0":
                       dec = dec_tem
                if out_line[2] == "year" and out_line[1] != "000":        
                    year_pred = cent_dec_pred(out_line[1], cent, dec)
                    out_line.append(year_pred)
                elif out_line[4] == "year" and out_line[3] != "000":        
                    year_pred = cent_dec_pred(out_line[3], cent, dec)
                    out_line.append(year_pred)
                else:
                    out_line.append(False)
                
                # Caclulating years pre author and registering negatives as errors
                if out_line[5] is not False:
                    pre_date = int(d_date) - int(out_line[5])                    
                    if pre_date < 0:
                        neg = True
                        neg_c = neg_c + 1
                    str_pre = str(pre_date)
                    if len(str_pre) == 2:
                        str_pre = '0' + str_pre
                    if len(str_pre) == 1:
                        str_pre = '00' + str_pre
                else:
                    str_pre = False
                
                    
                # Writing line wordcount and full line to output
                out_line.append(str_pre)
                out_line.append('1')
                out_line.append(toks)
                # Adding into full_stats
                if out_line[5] is not False:
                    for date_ent in full_stats:
                        if date_ent[0] == out_line[5]:
                        
                           date_ent[1] = date_ent[1] + 1
                           date_ent[2] = date_ent[2] + toks
                           break
                if out_line[6] is not False:
                    for date_pre in full_stats_pre:
                        if date_pre[0] == out_line[6]:
                        
                            date_pre[1] = date_pre[1] + 1
                            date_pre[2] = date_pre[2] + toks
                            break
                out.append(out_line)
    
                # Check level 2
                if max_l >= 2:
                    
                    l2 = md_seg(sect, 2)
                    for sect_2 in l2:
                        print('.', end = '')
                        md_header = re.findall(r"(###.+\n)", sect_2)
                        
                        toks = count(sect_2)
                        out_line = line_y_tag(md_header[0], csv)
            
                        # Predicting actual dates
                        if out_line[2] == "year":
                            cent_tem = cent_loc(out_line[1])
                            dec_tem = dec_loc(out_line[1])
                            if cent_tem != "0":
                                cent = cent_tem
                                dec = dec_tem
                            if cent_tem == "0" and dec_tem != "0":
                                dec = dec_tem
                        if out_line[4] == "year":
                            cent_tem = cent_loc(out_line[3])
                            dec_tem = dec_loc(out_line[3])
                            if cent_tem != "0":
                                cent = cent_tem
                                dec = dec_tem
                            if cent_tem == "0" and dec_tem != "0":
                                dec = dec_tem
                        if out_line[2] == "year" and out_line[1] != "000":        
                                year_pred = cent_dec_pred(out_line[1], cent, dec)
                                out_line.append(year_pred)
                        elif out_line[4] == "year" and out_line[3] != "000":        
                                year_pred = cent_dec_pred(out_line[3], cent, dec)
                                out_line.append(year_pred)
                        else:
                            out_line.append(False)
                        
                        # Caclulating years pre author and registering negatives as errors
                        if out_line[5] is not False:
                            pre_date = int(d_date) - int(out_line[5])                            
                            if pre_date < 0:
                                neg = True
                                neg_c = neg_c + 1
                            str_pre = str(pre_date)
                            if len(str_pre) == 2:
                                str_pre = '0' + str_pre
                            if len(str_pre) == 1:
                                str_pre = '00' + str_pre
                                
                        else:
                            str_pre = False
                    
                    
                        # Writing line wordcount and full line to output
                        out_line.append(str_pre)
                        out_line.append('2')
                        out_line.append(toks)
                        # Adding into full_stats
                        if out_line[5] is not False:
                            for date_ent in full_stats:
                                if date_ent[0] == out_line[5]:
                        
                                    date_ent[1] = date_ent[1] + 1
                                    date_ent[2] = date_ent[2] + toks
                                    
                                    break
                        if out_line[6] is not False:                            
                            for date_pre in full_stats_pre:
                                
                                if date_pre[0] == out_line[6]:
                        
                                    date_pre[1] = date_pre[1] + 1
                                    date_pre[2] = date_pre[2] + toks
                                    
                                    break
                        
                        out.append(out_line)
                        
                        # Check level 3
                        if max_l >=3:
                            l3 = md_seg(sect_2, 3)
                            for sect_3 in l3:                                
                                md_header = re.findall(r"(###.+\n)", sect_3)
                                toks = count(sect_3)
                                out_line = line_y_tag(md_header[0], csv)
                   
                                # Predicting actual dates
                                if out_line[2] == "year":
                                    cent_tem = cent_loc(out_line[1])
                                    dec_tem = dec_loc(out_line[1])
                                    if cent_tem != "0":
                                        cent = cent_tem
                                        dec = dec_tem
                                    if cent_tem == "0" and dec_tem != "0":
                                        dec = dec_tem
                                if out_line[4] == "year":
                                    cent_tem = cent_loc(out_line[3])
                                    dec_tem = dec_loc(out_line[3])
                                    if cent_tem != "0":
                                        cent = cent_tem
                                        dec = dec_tem
                                    if cent_tem == "0" and dec_tem != "0":
                                        dec = dec_tem
                                if out_line[2] == "year" and out_line[1] != "000":        
                                    year_pred = cent_dec_pred(out_line[1], cent, dec)
                                    out_line.append(year_pred)
                                elif out_line[4] == "year" and out_line[3] != "000":        
                                    year_pred = cent_dec_pred(out_line[3], cent, dec)
                                    out_line.append(year_pred)
                                else:
                                    out_line.append(False)
                                    
                                # Caclulating years pre author and registering negatives as errors
                                if out_line[5] is not False:
                                    pre_date = int(d_date) - int(out_line[5])                            
                                    if pre_date < 0:
                                        neg = True
                                        neg_c = neg_c + 1
                                    str_pre = str(pre_date)
                                    if len(str_pre) == 2:
                                        str_pre = '0' + str_pre
                                    if len(str_pre) == 1:
                                        str_pre = '00' + str_pre
                                else:
                                    str_pre = False
                    
                    
                                # Writing line wordcount and full line to output
                                out_line.append(str_pre)
                                out_line.append('3')
                                out_line.append(toks)
                                # Adding into full_stats
                                if out_line[5] is not False:
                                    for date_ent in full_stats:
                                        if date_ent[0] == out_line[5]:
                        
                                            date_ent[1] = date_ent[1] + 1
                                            date_ent[2] = date_ent[2] + toks
                                            break
                                if out_line[6] is not False:
                                   for date_pre in full_stats_pre:
                                       if date_pre[0] == out_line[6]:
                        
                                           date_pre[1] = date_pre[1] + 1
                                           date_pre[2] = date_pre[2] + toks
                                           break
                                
                                out.append(out_line)
                                # Check level 4
                                if max_l >=4:
                                    l4 = md_seg(sect_3, 4)
                                    for sect_4 in l4:
                                        md_header = re.findall(r"(###.+\n)", sect_4)
                                        toks = count(sect_4)
                                        out_line = line_y_tag(md_header[0], csv)
                   
                                        # Predicting actual dates
                                        if out_line[2] == "year":
                                            cent_tem = cent_loc(out_line[1])
                                            dec_tem = dec_loc(out_line[1])
                                            if cent_tem != "0":
                                                cent = cent_tem
                                                dec = dec_tem
                                            if cent_tem == "0" and dec_tem != "0":
                                                dec = dec_tem
                                        if out_line[4] == "year":
                                            cent_tem = cent_loc(out_line[3])
                                            dec_tem = dec_loc(out_line[3])
                                            if cent_tem != "0":
                                                cent = cent_tem
                                                dec = dec_tem
                                            if cent_tem == "0" and dec_tem != "0":
                                                dec = dec_tem
                                        if out_line[2] == "year" and out_line[1] != "000":        
                                            year_pred = cent_dec_pred(out_line[1], cent, dec)
                                            out_line.append(year_pred)
                                        elif out_line[4] == "year" and out_line[3] != "000":        
                                            year_pred = cent_dec_pred(out_line[3], cent, dec)
                                            out_line.append(year_pred)
                                        else:
                                            out_line.append(False)
                            
                                        # Caclulating years pre author and registering negatives as errors
                                        if out_line[5] is not False:
                                            pre_date = int(d_date) - int(out_line[5])                            
                                            if pre_date < 0:
                                                neg = True
                                                neg_c = neg_c + 1
                                            str_pre = str(pre_date)
                                            if len(str_pre) == 2:
                                                str_pre = '0' + str_pre
                                            if len(str_pre) == 1:
                                                str_pre = '00' + str_pre
                                            else:
                                                str_pre = False
                    
                    
                                        # Writing line wordcount and full line to output
                                        out_line.append(str_pre)
                                        out_line.append('4')
                                        out_line.append(toks)
                                        # Adding into full_stats
                                        if out_line[5] is not False:
                                            for date_ent in full_stats:
                                                if date_ent[0] == out_line[5]:
                        
                                                    date_ent[1] = date_ent[1] + 1
                                                    date_ent[2] = date_ent[2] + toks
                                                    break
                                        if out_line[6] is not False:        
                                            for date_pre in full_stats_pre:
                                                if date_pre[0] == out_line[6]:
                        
                                                    date_pre[1] = date_pre[1] + 1
                                                    date_pre[2] = date_pre[2] + toks
                                                    break
                                        out.append(out_line)
                            
                                        # Checking and writing level 5
                                        if max_l >= 5:
                                            l5 = md_seg(sect_4, 5)
                                            for sect_5 in l5:
                                                md_header = re.findall(r"(###.+\n)", sect_5)
                                                toks = count(sect_5)
                                                out_line = line_y_tag(md_header[0], csv)
                   
                                                # Predicting actual dates
                                                if out_line[2] == "year":
                                                    cent_tem = cent_loc(out_line[1])
                                                    dec_tem = dec_loc(out_line[1])
                                                    if cent_tem != "0":
                                                        cent = cent_tem
                                                        dec = dec_tem
                                                    if cent_tem == "0" and dec_tem != "0":
                                                        dec = dec_tem
                                                if out_line[4] == "year":
                                                    cent_tem = cent_loc(out_line[3])
                                                    dec_tem = dec_loc(out_line[3])
                                                    if cent_tem != "0":
                                                        cent = cent_tem
                                                        dec = dec_tem
                                                    if cent_tem == "0" and dec_tem != "0":
                                                        dec = dec_tem
                                                if out_line[2] == "year" and out_line[1] != "000":        
                                                    year_pred = cent_dec_pred(out_line[1], cent, dec)
                                                    out_line.append(year_pred)
                                                elif out_line[4] == "year" and out_line[3] != "000":        
                                                    year_pred = cent_dec_pred(out_line[3], cent, dec)
                                                    out_line.append(year_pred)
                                                else:
                                                    out_line.append(False)
                            
                                               # Caclulating years pre author and registering negatives as errors
                                                if out_line[5] is not False:
                                                    pre_date = int(d_date) - int(out_line[5])                            
                                                    if pre_date < 0:
                                                        neg = True
                                                        neg_c = neg_c + 1
                                                    str_pre = str(pre_date)
                                                    if len(str_pre) == 2:
                                                        str_pre = '0' + str_pre
                                                    if len(str_pre) == 1:
                                                        str_pre = '00' + str_pre
                                                    else:
                                                        str_pre = False
                    
                    
                                               # Writing line wordcount and full line to output
                                                out_line.append(str(str_pre))
                                                out_line.append('5')
                                                out_line.append(toks)
                                                # Adding into full_stats
                                                if out_line[5] is not False:
                                                    for date_ent in full_stats:
                                                        if date_ent[0] == out_line[5]:
                        
                                                            date_ent[1] = date_ent[1] + 1
                                                            date_ent[2] = date_ent[2] + toks
                                                            break
                                                if out_line[6] is not False:
                                                    for date_pre in full_stats_pre:
                                                        if date_pre[0] == out_line[6]:
                        
                                                            date_pre[1] = date_pre[1] + 1
                                                            date_pre[2] = date_pre[2] + toks
                                                            break
                                                out.append(out_line)
                                    
                                                # Checking and writing level 6
                                                if max_l >= 6:
                                                    l6 = md_seg(sect_5, 6)
                                                    for sect_6 in l6:
                                                        md_header = re.findall(r"(###.+\n)", sect_6)
                                                        toks = count(sect_6)
                                                        out_line = line_y_tag(md_header[0], csv)
                   
                                                        # Predicting actual dates
                                                        if out_line[2] == "year":
                                                            cent_tem = cent_loc(out_line[1])
                                                            dec_tem = dec_loc(out_line[1])
                                                            if cent_tem != "0":
                                                                cent = cent_tem
                                                                dec = dec_tem
                                                            if cent_tem == "0" and dec_tem != "0":
                                                                dec = dec_tem
                                                        if out_line[4] == "year":
                                                            cent_tem = cent_loc(out_line[3])
                                                            dec_tem = dec_loc(out_line[3])
                                                            if cent_tem != "0":
                                                                cent = cent_tem
                                                                dec = dec_tem
                                                            if cent_tem == "0" and dec_tem != "0":
                                                                dec = dec_tem
                                                        if out_line[2] == "year" and out_line[1] != "000":        
                                                            year_pred = cent_dec_pred(out_line[1], cent, dec)
                                                            out_line.append(year_pred)
                                                        elif out_line[4] == "year" and out_line[3] != "000":        
                                                            year_pred = cent_dec_pred(out_line[3], cent, dec)
                                                            out_line.append(year_pred)
                                                        else:
                                                            out_line.append(False)
                            
                                                       # Caclulating years pre author and registering negatives as errors
                                                        if out_line[5] is not False:
                                                            pre_date = int(d_date) - int(out_line[5])                            
                                                            if pre_date < 0:
                                                                neg = True
                                                                neg_c = neg_c + 1
                                                            str_pre = str(pre_date)
                                                            if len(str_pre) == 2:
                                                                str_pre = '0' + str_pre
                                                            if len(str_pre) == 1:
                                                                str_pre = '00' + str_pre
                                                        else:
                                                            str_pre = False
                    
                    
                                                        # Writing line wordcount and full line to output
                                                        out_line.append(str_pre)
                                                        out_line.append('6')
                                                        out_line.append(toks)
                                                        # Adding into full_stats
                                                        if out_line[5] is not False:
                                                            for date_ent in full_stats:
                                                                if date_ent[0] == out_line[5]:
                        
                                                                    date_ent[1] = date_ent[1] + 1
                                                                    date_ent[2] = date_ent[2] + toks
                                                                    break
                                                        if out_line[6] is not False:
                                                            for date_pre in full_stats_pre:
                                                                if date_pre[0] == out_line[6]:
                        
                                                                    date_pre[1] = date_pre[1] + 1
                                                                    date_pre[2] = date_pre[2] + toks
                                                                    break
                                                        out.append(out_line)
                            
                            
            
            print('')
            out_path = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Date tagger tests/Full_corpus_25_10/Out_pre_text/" + file_name + ".csv"
            
            tags_out_df = pd.DataFrame(out, columns = ["string", "date", "year_type", "date_2", "year_type_2", "predicted_year", "years_pre", "md_level", "section word count"])
            tags_out_df.to_csv(path_or_buf = out_path, index=False, encoding= "utf-8-sig")
            if neg:
                rep = []
                rep.append(name)
                rep.append(neg_c)
                error_rep.append(rep)

full_stats_df = pd.DataFrame(full_stats, columns = ["Date", "Header_count", "Word_count"])
full_stats_df.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Date tagger tests/Full_corpus_25_10/Out_summary/full_stats.csv", index=False, encoding= "utf-8-sig")

full_stats_pre_df = pd.DataFrame(full_stats_pre, columns = ["Date_Before", "Header_count", "Word_count"])
full_stats_pre_df.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Date tagger tests/Full_corpus_25_10/Out_summary/pre_author_dates_stats.csv", index=False, encoding= "utf-8-sig")

error_rep_df = pd.DataFrame(error_rep, columns = ["text", 'negative count'])
error_rep_df.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Date tagger tests/Full_corpus_25_10/Out_summary/error_rep.csv", index=False, encoding = 'utf-8-sig')
    