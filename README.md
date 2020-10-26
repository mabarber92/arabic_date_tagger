# arabic_date_tagger
Experiments to use a script to tag dates within an Arabic corpus

### Basic summary

This repository contains the script used to tag dates from mARKdown headings in the OpenITI corpus (instance downloaded from GitHub on 25/10/2020). The script uses a dataframe containing Arabic numbers and their corresponding numerals and uses these to convert the dates within texts into numerals.

### Repository structure

**tagged_for_run_25_10.py** is the instance of the script used for the run.
**dates df.csv** is a list of Arabic numbers and corresponding numerals for the script.

**Out_pre_text** gives a csv for every primary text on the OpenITI corpus, listing mARkdown and the corresponding dates. Each file gives up to two dates pre heading and differentiates between date types. 'Predicted_year' gives an adjusted date based on the preceding dates (to account for where chroniclers have dropped the hundred from the number) *Caution: this figure is likely to be wrong for texts that are not organised chronologically* 'years_pre' gives the number of years that the predicted date occurred prior to the author's death (using OpenITI URI death dates).

**Out_summary** gives two full corpus summary files. The first 'full_stats' lists all of the dates mentioned in the corpus, the number of maRKdown headings given for the date and the number of words written under that date. 'pre_author_dates_stats' gives the same totals for the number of years prior to an author's death.

**Analysis** provides the scripts used for analysising the full corpus data and some basic analysis and graphs.


### Acknowledgement
This work is reliant on the [OpenITI corpus](github.com/openiti) and its machine-readable texts and its structural annotation that is only available thanks to the painstaking work of annotators. Without this annotation, it would not be possible to do this kind of analysis.

#### Disclaimer
This is a work in progress. This outputs are likely to contain errors. If you spot an issue, please report it in the issues.
