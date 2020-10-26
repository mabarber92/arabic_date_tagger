# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 15:45:04 2020

@author: mathe
"""
import pandas as pd
import matplotlib.pyplot as plt
import statistics as st

years = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Date tagger tests/Full_corpus_25_10/Out_summary/pre_author_dates_stats.csv")

def rolling_ave(df, interval):
    
    list_val = df.values.tolist()
    
    averages = []
    count = 0
    for x in range(interval, 1000, interval):
        line = []
        val_list = []
        for item in list_val[count:x]:
            val_list.append(item[1])
    
        mean = st.mean(val_list)    
        summed = sum(val_list)
    
        line.append(count)
        line.append(mean)
        line.append(summed)
        averages.append(line)
        count = count + interval
    ave_word_df = pd.DataFrame(averages, columns = ["Date", "Average", "Total"])
    return ave_word_df

def ave_hwc_roll (df, interval):
    list_val = df.values.tolist()
    averages = []
    count = 0
    for x in range(interval, 1000, interval):
        line = []
        val_list = []
        
        for item in list_val[count:x]:
            
            if item[1] != 0 and item[2] != 0:
                per_line = item[2]/item[1]
                
            else:
                per_line = 0
            val_list.append(per_line)
        
        
        mean = st.mean(val_list)    
        summed = sum(val_list)
    
        line.append(count)
        line.append(mean)
        line.append(summed)
        averages.append(line)
        count = count + interval
    ave_word_df = pd.DataFrame(averages, columns = ["Date", "Average_per_line", "Total_per_line"])
    return ave_word_df

def stacker (df, interval):            
    list_val = df.values.tolist()
    stacked = []
    count = 0
    label_c = 0
    label = ["Date"]
    for x in range(0, interval):
        label_c = label_c + 1
        label.append(str(label_c))
    for x in range(interval, 1000, interval):
        line = []
        line.append(count)
        for item in list_val[count:x]:
            line.append(item[1])
        stacked.append(line)
        count = count + interval
    stacked_df = pd.DataFrame(stacked, columns = label)
    return stacked_df  

def ave_stacker (df, interval):            
    list_val = df.values.tolist()
    stacked = []
    count = 0
    label_c = 0
    label = ["Date"]
    for x in range(0, interval):
        label_c = label_c + 1
        label.append(str(label_c))
    for x in range(interval, 1000, interval):
        line = []
        line.append(count)
        for item in list_val[count:x]:
            if item[1] != 0 and item[2] != 0:
                per_line = item[2]/item[1]
                
            else:
                per_line = 0
            line.append(per_line)
        stacked.append(line)
        count = count + interval
    stacked_df = pd.DataFrame(stacked, columns = label)
    return stacked_df       

word_count = years[["Date", "Word_count"]]
head_count = years[["Date", "Header_count"]]

word_count_ave = rolling_ave(word_count, 25)
head_count_ave = rolling_ave(head_count, 25)

word_count_stack = stacker(word_count, 25)
ave_word_stack = ave_stacker (years, 25)


wc_per_head = ave_hwc_roll(years, 25)




word_count_ave[["Date", "Average"]].plot.bar(x = "Date")
word_count_ave[["Date", "Total"]].plot.bar(x = "Date")
head_count_ave[["Date", "Average"]].plot.bar(x = "Date")
head_count_ave[["Date", "Total"]].plot.bar(x = "Date")

wc_per_head[["Date", "Average_per_line"]].plot.bar(x= "Date")
wc_per_head[["Date", "Total_per_line"]].plot.bar(x="Date")

word_count_stack.plot.bar(x = "Date", stacked = True, legend = False, title = "Total word counts for number of years before author's death, sorted into columns of 25 years")
plt.savefig("word_count_stack_pre.png", dpi=300, bbox_inches='tight')
ave_word_stack.plot.bar(x = "Date", stacked = True, legend = False, title = "Word counts per header for number of years before author's death, sorted into columns of 25 years")
plt.savefig("ave_word_stack_pre.png", dpi=300, bbox_inches='tight')

max_word = years.nlargest(20, "Word_count", keep="all").sort_values("Date")
max_head = years.nlargest(20, "Header_count", keep="all").sort_values("Date")
min_word = years.nsmallest(20, "Word_count", keep="all").sort_values("Date")
min_word_pre_900 = years[0:899].nsmallest(20, "Word_count", keep = "all").sort_values("Date")
max_word_post_100 = years[100:].nlargest(20, "Word_count", keep="all").sort_values("Date")
max_word.to_csv("max_word_pre.csv", index=False)
min_word.to_csv("min_word_pre.csv", index=False)
max_head.to_csv("max_head_pre.csv", index=False)
min_word_pre_900.to_csv("min_word_pre_900_pre.csv", index = False)
max_word_post_100.to_csv("max_word_post_100_pre.csv", index = False)