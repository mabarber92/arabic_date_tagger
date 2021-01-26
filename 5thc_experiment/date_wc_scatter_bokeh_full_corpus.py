# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 12:16:17 2021

@author: mathe
"""

import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Legend
from bokeh.palettes import Category20, Spectral4
import pandas as pd
import numpy as np
import statistics as st

def clean_select (df_csv, start, end, cols = ["string", "evaluation_year", "md_level", "section_word_count", "URI", "Author", "Book", "Death_date", "heading_two_dates"]):
    
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

def annual_ave_median(clean_df):
    list_dates = clean_df["predicted_year"].drop_duplicates()
    list_out = []
    for date in list_dates:
        word_counts = clean_df.loc[clean_df["predicted_year"] == date]["section word count"]
        mean = st.mean(word_counts)
        median = st.median(word_counts)
        list_out.append([date, mean, median])
    out_df = pd.DataFrame(list_out, columns = ["Date", "Mean", "Median"])
    out_df = out_df.sort_values(by=["Date"])
    return out_df

def author_plotter_bok(clean_df, out, averages_df = None, hue = True, field = 'URI', log = None, tt = None, fig_w = 1400, fig_h = 700, alpha = 0.3):

    # Import data    
    dates_df = clean_df
    dates_df["word_count"] = dates_df["section word count"].astype(int)
        
    
    # Adding selected tool_tips
    tool_tips = tt
    
    p = figure(plot_width = fig_w, plot_height = fig_h, tooltips = tool_tips, title = "Dates mentioned by each author against their word count in the full corpus (Click in legend to remove mean or median lines). Hover on points to see Author name and book title.")
    p.add_layout(Legend(), 'right')
    
    # Creating plot
    source = ColumnDataSource(dates_df)
    
   
    p.circle("predicted_year", "section word count", source = source, color = "orange", alpha = alpha)
    

    
    
    # Adding mean and median lines if requested
    if not averages_df.empty:
        
        p.line(averages_df["Date"], averages_df["Mean"], color = Spectral4[0], legend_label= "Mean")
        p.line(averages_df["Date"], averages_df["Median"], color = Spectral4[3], legend_label = "Median")

    p.legend.click_policy = "hide"    
    
    output_file(out)

    show(p)
    
data = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/bokeh trial/full_dates2")

mean_date = annual_ave_median(data)

author_plotter_bok(data, "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/bokeh trial/full_corpus_scatter.html", mean_date, tt = [("Author", "@Author"), ("Book", "@Book"), ("Year", "@predicted_year"), ("Word Count", "@word_count"), ("death date", "@Death_date")])

