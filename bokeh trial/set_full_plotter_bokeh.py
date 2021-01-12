# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:27:46 2021

@author: mathe
"""

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd
import numpy as np

dates_df = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/bokeh trial/full_dates.csv")[["predicted_year", "section word count", "Author", "Book", "Death_date"]]
dates_df["section word count"].astype(int)
dates_df_scaled = dates_df
dates_df_scaled["sizes"] = np.log2(dates_df_scaled["section word count"])
dates_df_scaled["word_count"] = dates_df["section word count"]

source = ColumnDataSource(dates_df_scaled)
death_date = ColumnDataSource({"x": [0, 1400], "y": [0, 1400]})
pre_50_ddate = ColumnDataSource({"x": [0, 1400], "y": [50, 1450]})
pre_100_ddate = ColumnDataSource({"x": [0, 1400], "y": [100, 1500]})
pre_200_ddate = ColumnDataSource({"x": [0, 1400], "y": [200, 1700]})

tool_tips = [("Author", "@Author"), ("Book", "@Book"), ("Year", "@predicted_year"), ("Word Count", "@word_count")]

p = figure(plot_width = 1800, plot_height = 800, tooltips = tool_tips, title = "Dates mentioned by author and book and their death date")

p.circle('predicted_year', 'Death_date', size = ("sizes"), source = source, alpha = 0.3)
p.line("x", "y", source = death_date, color = "red")
p.line("x", "y", source = pre_50_ddate, color = "green")
p.line("x", "y", source = pre_100_ddate, color = "orange")
p.line("x", "y", source = pre_200_ddate, color = "purple")

output_file("Dates_deathdate_comp.html")

show(p)