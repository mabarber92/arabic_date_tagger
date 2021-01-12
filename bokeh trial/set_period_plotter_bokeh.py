# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:27:46 2021

@author: mathe
"""

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd

dates_df = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/bokeh trial/period_dates.csv")


source = ColumnDataSource(dates_df)

tool_tips = [("Author", "@Author"), ("Book", "@Book"), ("Word Count", "@Word_count")]

p = figure(plot_width = 1000, plot_height = 400, tooltips= tool_tips, title = "Fifty Year periods by author and their death date")

p.circle('50 Year Period', 'Death_date', source = source)

output_file("50 year periods.html")

show(p)