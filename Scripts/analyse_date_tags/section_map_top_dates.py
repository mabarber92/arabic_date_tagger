from pattern_mapping_cat import pattern_map_dates
from count_distinct_features import count_y_centuries
import pandas as pd

def section_map_top_dates(text_path, section_map_out, input_csv = None, ranking_slice = 10):
    """If input_type is csv then we will proceed directly to using csv for ranking. If it is 'text' then we will get a df from the text using the
    count_distinct_features. If it is "text_path" we will open the text before passing it to the function
    NOTE NEED TO FIX THE count_y_centuries for the text input to work properly"""
    with open(text_path, encoding='utf-8') as f:
        text = f.read()
    if input_csv is None:        
        # Add count_y_centuries once function is fixed
        print("WARNING: text input not configured - count_y_centuries needs refactoring")
    else:
        ranking_df = pd.read_csv(input_csv)
        
    # Make sure that the df is sorted by the distinct count
    ranking_df = ranking_df.sort_values(by=["Distinct count"], ascending=False)

    # Take the top rank according to spec
    date_list = ranking_df.iloc[:ranking_slice]["date"].to_list()
    date_list = ["@YY" + str(x).zfill(3) for x in date_list]
    print(date_list)

    section_map = pattern_map_dates(text, add_terms = date_list, w_counts=True, add_section_title=True)

    section_map.to_csv(section_map_out, encoding='utf-8-sig', index=False)

if __name__ == "__main__":
    text_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/release-08-09-2022/texts_date_tagged/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged"
    csv_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/release-08-09-2022/dates_data/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged.all_dates_distinct.csv"
    out_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/release-08-09-2022/dates_data/0845Maqrizi.Mawaciz.MAB02082022.sections-top10-dates.csv"
    section_map_top_dates(text_path, out_path, input_csv=csv_path)
