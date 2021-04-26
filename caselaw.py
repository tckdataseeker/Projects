# Run the below to graph the historical frequency of words present in cases stored in the CaseLaw API (https://case.law/). 
# You may search keywords based on the race and the crime you would like to inquire about.

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import re

def main():
    def date_validate(datestring):
        try:
            datetime.strptime(datestring, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def keyword_search(text, keywords_to_search):
        
        keywords_to_search = list(keywords_to_search.split())
        for keyword in keywords_to_search:
            regex = re.compile(keyword)
            count_hit = len(regex.findall(text, re.IGNORECASE))
            #count_hit = len(re.findall(keyword,text, re.IGNORECASE))
        return count_hit > 0

    race = input('Enter the race you would like to query (enter a single word): ')
    crime = input('Enter the crime type you would like to query (enter a single word): ')
    response_crime_by_race = requests.get(
        'https://api.case.law/v1/cases/?search=' + str(crime) + ' ' +  str(race)+'&full_case=true&page_size=10000',
        headers={'Authorization': '1929e96bcc41077d918520a9e1f888bbc25550ff'}
        )
    
    case_id =  [case['id'] for case in response_crime_by_race.json()['results']]
    case_year  = [datetime.strptime(case['decision_date'],"%Y-%m-%d").year  if date_validate(case['decision_date']) else int(case['decision_date'][0:4]) for case in response_crime_by_race.json()['results']]
    case_jur = [case['jurisdiction']['name_long'] for case in response_crime_by_race.json()['results']]

    case_prvw = []
    for case in response_crime_by_race.json()['results']:
        prvw_text = ' '.join(case['preview'])
        soup = BeautifulSoup(prvw_text, "html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
            
        # get text
        text = str(soup.get_text())
        case_prvw.append(text)

    df = pd.DataFrame({'id':case_id, 'year': case_year, 'jurisdiction': case_jur, 'case_text_preview': case_prvw})

    keywords = input('Enter keywords you would like to search (separate each keyword by space): ')
    keyword_columns = keywords.split()

    for keyword in keyword_columns:
        df[keyword] = df['case_text_preview'].apply(lambda x: 1 if keyword_search(x, keyword) >=1 else 0)
    
    df_agg = df.groupby(['year']).sum()
    df_count = df.groupby('year').agg({'id':pd.Series.nunique})

    # plot data
    fig = plt.figure() #creae a figure object
    ax = fig.add_axes([.15,.15,.7,.7])
    for kw in keyword_columns:
        ax.plot(df_agg.index,df_agg[kw], label=kw)
    ax.plot(df_count.index, df_count['id'], label = '# of cases')
        
    ax.set_title('Number of ' + str(crime) + ' cases citing ' + str(race) + ' race by year')
    ax.set_xlabel('Year')
    plt.xticks(rotation = 45)
    ax.set_ylabel('Frequency')
    plt.grid(b=True, which='major', axis='both')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
