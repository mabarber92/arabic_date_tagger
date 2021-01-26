# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:23:32 2021

@author: mathe
"""
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, LinearColorMapper
import pandas as pd
import numpy as np

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


def author_plotter_bok(clean_df, out, size = True, hue = True, log = None, tt = None, fig_w = 1400, fig_h = 700, alpha = 0.3):

    # Import data    
    dates_df = clean_df
    
    # If log is being used - apply to section word counts
    if size:    
        if log == 2:
            dates_df["sizes"] = np.log2(dates_df["section_word_count"])
    
    # If no log - ensure that sizes is same as word count and is an int
        if log == None:
            dates_df["sizes"] = dates_df["section_word_count"].astype(int)/100
    else:
        dates_df["sizes"] = 15
    
    

    # Applying shaded colour pallett for word counts    
    if hue:
        color_mapper = LinearColorMapper(palette = "Category10_10", low=min(dates_df["section_word_count"]), high=max(dates_df["section_word_count"]))
        colors = {"field": 'section_word_count', 'transform': color_mapper}
    else:
        colors = "blue"
        
    
    # Adding selected tool_tips
    tool_tips = tt
    
    
    
    
    source = ColumnDataSource(dates_df)
    
    # Creating plot
    p = figure(plot_width = fig_w, plot_height = fig_h, tooltips = tool_tips, title = "Dates mentioned by author and book and their death date")
    
    p.circle('evaluation_year', 'Death_date', size = ("sizes"), source = source, alpha = alpha, color = colors)
    
    output_file(out)

    show(p)

data = clean_select("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Data/5thc_evaluations2.csv", 390, 520)

author_plotter_bok(data, "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/5thc_experiment/Visualisations/5th_c_plot.html", log = 2, tt = [("Author", "@Author"), ("Book", "@Book"), ("Year", "@evaluation_year"), ("Word Count", "@section_word_count"), ("string", "@string"), ("death date", "@Death_date")], size = False)