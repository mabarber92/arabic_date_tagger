# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 08:57:02 2021

@author: mathe
"""
import pandas as pd
import re
import os

def period_select (URI, df_in, df_to_write, start, end):
    # Separating URI into metadata
   
    date_author, book, book_id = tuple(URI.split("."))
    d_date, author, bln = tuple(re.findall(r"\d{4}|[a-zA-Z]*", date_author))
    d_date = str(d_date)
    
    
    # Only working with files where death date exceeds end of range
    if int(d_date) > end:
        # Taking rows with predicted dates within specified period
        list_rows = df_in.values.tolist()
        found_start = False
    
        out_rows = []
    
        range_dates = []
        for x in range(start,end):
            range_dates.append(x)
    
        
        for date in range_dates:
            if found_start:
                break
            for idx, row in enumerate(list_rows):
                try:
                    if int(row[5]) == date:
                        print(date)
                        start_pos = idx-1
                        found_start = True
                    
                except ValueError:
                    continue
    
        if found_start:
        
            for row in list_rows[start_pos:-1]:
                try:
                    if int(row[5]) < end:
                        out_rows.append(row)
                    if int(row[5]) >= end:
                        out_rows.append(row)
                        break
                except ValueError:
                    out_rows.append(row)
                    continue
    
            print("dates in range found")
            df_to_concat = pd.DataFrame(out_rows, columns = ["string","date","year_type","date_2", "year_type_2", "predicted_year","years_pre","md_level","section word count"])
    
    
            # Adding metadata to ranged df
            df_to_concat["Author"] = author
            df_to_concat["Book"] = book
            df_to_concat["Death_date"] = d_date
            df_to_concat["URI"] = URI            
    
            # Concatenating with out df
            df_to_write = pd.concat([df_to_write, df_to_concat], sort = False)
   
    
    return df_to_write



# Running function on the dates files 

directory = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/Full_corpus_21_01/corpus_full"

os.chdir(directory)

out = pd.DataFrame() 

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        print("working on..." + name)
        URI = re.findall(r"(.*ara\d)", name)[0]
        path_e = os.path.join(root, name)
        path = os.path.abspath(path_e)
        df_in = pd.read_csv(path)
        
        if df_in.empty:
            print("empty dataframe... skipping")
            continue
        out = period_select(URI, df_in, out, 390, 520)

out.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/5thc_for_eval2.csv", index=False, encoding= "utf-8-sig")
    
