
import pandas as pd

dates_df = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/year skipping trial/skip_record.csv")

dates_filter = dates_df[(dates_df["abnormal_gap"] == False)]
dates_filter = dates_filter[(dates_filter["reverse"] == False)]

gap_first = dates_filter["gap_first"].values.tolist()
dates_set = set(gap_first)
counts = []

for value in dates_set:
    counts_line = [value]
    count = 0
    for date in gap_first:
        if date == value:
            count = count + 1
    counts_line.append(count)
    counts.append(counts_line)
    


# Use most common to subset the df and create subset list

counts_large = []

for count in counts:
    if count[1] >= 2:
        counts_large.append(count[0])
        
    
subset_df = dates_df[dates_df.gap_first.isin(counts_large)]

print(subset_df)

subset_df = subset_df.sort_values(by = ['gap_first'])
                     
subset_df.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/year skipping trial/skips_2_or_over.csv", encoding = "utf-8-sig", index = False)
        
    