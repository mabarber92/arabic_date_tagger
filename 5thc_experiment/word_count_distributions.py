# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:57:12 2021

@author: mathe
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def clean_select (df_csv, start, end, cols = ["string", "evaluation_year", "md_level", "section_word_count", "Author", "Book", "Death_date", "URI", "heading_two_dates"]):
    
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

def remove_infreq(df, freq = 10):
    # Creating lists of URIs
    uris_full = df["URI"].values.tolist()
    uris_sing = df["URI"].drop_duplicates().values.tolist()
    keep_list = uris_sing[:]
    
    # Creating list of URIs above chosen frequency
    for uri in uris_sing:
        count = uris_full.count(uri)
        if count <= freq:
            keep_list.remove(uri)

    # Building new df with those above set frequency    
    df_out = pd.DataFrame()
    
    for uri in keep_list:
        kept = df.loc[df["URI"] == uri]
        df_out = pd.concat([df_out, kept], sort = False)
    
    return df_out

def filter_below(df, cut):
    filtered = df.loc[df["section_word_count"] <= cut]
    return filtered

def basic_distr(df, sep = None):
    if sep == "uri":
        hues = df["URI"]
        element = "step"
    elif sep == "author":
        hues = df["Author"]
        element = "step"
    else:
        hues = None
        element = "bars"

    plot = sns.displot(x = "section_word_count", data = df, hue = hues, element = element)
    return plot


    
data = clean_select("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Data/5thc_evaluations2.csv", 390, 520)

data_more10 = remove_infreq(data)

data_under = filter_below(data, 2000)


plot1 = basic_distr(data)
plot2 = basic_distr(data_under)

plot1.savefig("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Visualisations/hist_all_no_sep.png", dpi= 400)
plot2.savefig("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Visualisations/hist_below_2000_no_sep.png", dpi= 400)

plt.clf()
plt.figure(figsize = [14, 10])
## sns.scatterplot(x = "evaluation_year", y = "section_word_count", data = data, hue = "URI", alpha = 0.7)


plot3 = sns.boxplot(x = "Book", y = "section_word_count", data = data_more10)
plt.xticks(rotation = 60)
plt.savefig("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Visualisations/box_plot.png", dpi= 400)

plt.show()



