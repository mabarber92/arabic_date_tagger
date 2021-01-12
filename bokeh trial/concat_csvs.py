import pandas as pd
import re
import os

def dates_concat (URI, df_in, df_to_write, df_per_to_write, period = 50, metadata = True, cols = ["predicted_year", "section word count"]):
    # Separating URI into metadata
    if metadata:
        date_author, book, book_id = tuple(URI.split("."))
        date, author, bln = tuple(re.findall(r"\d{4}|[a-zA-Z]*", date_author))
        date = str(date)
    # Subsetting df by required columns, trimming false values
    df_to_concat = df_in[cols]
    
    df_to_concat["predicted_year"] = df_to_concat["predicted_year"].astype(str)
    df_to_concat = df_to_concat.loc[df_to_concat.predicted_year.str.match("\d+")]
    df_to_concat["predicted_year"] = df_to_concat["predicted_year"].astype(int)
    # If metadata has been chosen, adding that info to the df
    if metadata:
        df_to_concat["Author"] = author
        df_to_concat["Book"] = book
        df_to_concat["Death_date"] = date
    df_to_concat["URI"] = URI
    # Concatenating with out df
    df_to_write = pd.concat([df_to_write, df_to_concat], sort = False)
    # Calculating lengths according to set period
    if not df_to_concat.empty:
        max_y = max(df_to_concat["predicted_year"].astype(int))
        iteration = int(max_y/period)
        year = 0
        step = 0
        first_iter = True
        date_periods = []
        for x in range(iteration):
            w_count = 0
            w_count_periods = []
            if not first_iter:
                step = step + period
            else:
                first_iter = False
            for y in range(period):
                count = 0
                row = df_to_concat.loc[df_to_concat["predicted_year"] == str(year)]
                try:
                    count = row[["section word count"]].values.tolist()[0][0]
                except IndexError:
                    pass                
                w_count = w_count + count
                year = year + 1
                if year == max_y:
                   break
            w_count_periods.append(step)
            w_count_periods.append(w_count)
            date_periods.append(w_count_periods)
        df_period = pd.DataFrame(date_periods, columns = [str(period) + " Year Period", "Word_count"])
        df_period = df_period[df_period.Word_count != 0]
        # Appending metadata to period df
        if metadata:
            df_period["Author"] = author
            df_period["Book"] = book
            df_period["Death_date"] = date
        df_period["URI"] = URI
        # Concatenating to the period df
        df_per_to_write = pd.concat([df_per_to_write, df_period], sort = False)
    
    return df_to_write, df_per_to_write
    

# 
directory = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/Full_corpus_25_10/Out_pre_text"

os.chdir(directory)

out = pd.DataFrame() 
out_per = pd.DataFrame() 

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        print("working on..." + name)
        URI = re.findall(r"(.*ara\d)", name)[0]
        path_e = os.path.join(root, name)
        path = os.path.abspath(path_e)
        df_in = pd.read_csv(path)
        if df_in.empty:
            print("no rows in dataframe... skipping")
            continue
        out, out_per = dates_concat(URI, df_in, out, out_per, period = 10)

out.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/bokeh trial/full_dates.csv", index=False, encoding= "utf-8-sig")
out_per.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/bokeh trial/period_dates_10.csv", index=False, encoding= "utf-8-sig")