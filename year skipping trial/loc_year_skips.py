
import pandas as pd



def loc_date_skip (df, surround = True, sur_dates = True):
    
    # Setting new df headings based on choices
    if surround:
        cols = ["gap_first", "gap_last", "abnormal_gap", "reverse", "Author", "Book", "Death_date", "URI", "prev_heading", "next_heading"]
    if sur_dates:
        cols = ["gap_first", "gap_last", "abnormal_gap", "reverse", "Author", "Book", "Death_date", "URI", "prev_date", "next_date"]
    if surround and sur_dates:
        cols = ["gap_first", "gap_last", "abnormal_gap", "reverse", "Author", "Book", "Death_date", "URI", "prev_heading", "next_heading", "prev_date", "next_date"]
    else:
        cols = ["gap_first", "gap_last", "abnormal_gap", "reverse", "Author", "Book", "Death_date", "URI"]
    
    # Creating output file
    out = []
    
    # Converting df to list
    list_df = df.values.tolist()
    
    # Iterating through to identify date skips
    for idx, row in enumerate(list_df):
        out_line = []
        URI = row[6]
        next_row = idx + 1
        # Checking next row doesn't belong to a different text        
        try:
            if list_df[next_row][6] == URI:
                # Calculate gap to next row
                next_year = list_df[next_row][0]
                gap = next_year - row[0]
                # If the gap is of one year continue to next iteraction
                if gap == 1 or gap == 0:
                    continue
                # Otherwise log the gap
                else:
                    gap_first = row[0] + 1
                    gap_last = next_year - 1
                    if gap > 25:
                        abnormal_gap = True
                    else:
                        abnormal_gap = False
                    if gap < 0:
                        reverse = True
                    else:
                        reverse = False
                    out_line.append(gap_first)
                    out_line.append(gap_last)
                    out_line.append(abnormal_gap)
                    out_line.append(reverse)
                    out_line.extend(row[3:7])
                    if surround:
                        out_line.append(row[2])
                        out_line.append(list_df[next_row][2])
                    if sur_dates:
                        out_line.append(row[0])
                        out_line.append(list_df[next_row][0])
                    out.append(out_line)
                    
            else:
                continue
        except IndexError:
            pass
        
    out_df = pd.DataFrame(out, columns = cols)
    return out_df
                

full_dates = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/year skipping trial/full_dates_string.csv")

out_df = loc_date_skip(full_dates)
out_df.to_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/year skipping trial/skip_record.csv", index=False, encoding= "utf-8-sig")
    
    