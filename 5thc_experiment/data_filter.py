# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:03:09 2021

@author: mathe
"""

import pandas as pd

def clean_select (df_csv, start, end, cols = ["string", "evaluation_year", "md_level", "section_word_count", "Author", "Book", "Death_date", "heading_two_dates"]):
    
    # Import csv
    data = pd.read_csv(df_csv)[cols]
    # Remove false values
    data["evaluation_year"] = data["evaluation_year"].astype(str)
    data = data.loc[data.evaluation_year.str.match("\d+")]
    data["evaluation_year"] = data["evaluation_year"].astype(int)
    
    # Filtering data to specified range
    data = data.loc[data.evaluation_year <= end]
    data = data.loc[data.evaluation_year >= start]
    
    return data


# Sample running function on df input
test = clean_select("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Data/5thc_evaluations2.csv", 390, 520)
