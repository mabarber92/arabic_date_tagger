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




    
data = clean_select("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Data/5thc_evaluations2.csv", 390, 520)


top_wc = data.loc[data["section_word_count"] >= 6000]

top_wc.to_csv("top_word_counts.csv", index = False, encoding = "utf-8-sig")
