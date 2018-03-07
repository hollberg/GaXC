"""config.py: configuration, lists to support the PiXC (pi cross country)"""
import requests
from bs4 import BeautifulSoup

# List Race Names and 'base' race URLs
races = {
    'State Meet:': 'http://ga.milesplit.com/meets/278506/results#.WeV2eBSLS_U',
    'Marist Meet': 'http://ga.milesplit.com/meets/280074/results#.Wdo95ZH3ahA',
    'Wingfoot Classic': 'http://ga.milesplit.com/meets/272824/results#.WchzXJH3ahA',
    'Whitfield': 'http://ga.milesplit.com/meets/263683/results#.Wba4q5H3ahA',
    'ATT meet': 'http://ga.milesplit.com/meets/282903/results#.Was1_JH3ahB',
    'Battle of Atlanta': 'http://ga.milesplit.com/meets/267314/results#.WaIimZH3ahA'
}

def get_soup(url):
    content = requests.get(url).content
    return BeautifulSoup(content, 'lxml')

# Relevant fields/columns to capture from each results site
headers = ['Rank', 'Name', 'Year', 'Team', 'Points', 'Time', 'Meet', 'Event', 'Link']

# fixed length formatting for "Fast Feet Timing" results
fast_feet_parse = {'Rank': slice(0,4),
                      'Name': slice(5,28),
                      'Year': slice(29,31),
                      # 'Number': slice(32,36),
                      'Team': slice(37,60),
                      'Points': slice(61,69),
                      'Time': slice(70,79),
                      # 'AvgMile': slice(80,90),
                      # 'AvgKm': slice(91,101),
}

# fixed-width layout for "Perfect Timing Group" and "Smart Event Mgmt" Results
perfect_timing_parse = {'Rank': slice(0,3),
                 'Name': slice(4, 29),
                 'Year': slice(30,32),
                 'Team': slice(33,54),
                 'Points': slice(65, 68),
                 'Time': slice(55,63),
                 #'Alternate': slice(69,72)
}

"""See link at: https://twitter.com/python_tip/status/966704808328646657
    # You can name your slices:
    >>> record = "01234567890123456789I want this0123456789"
    >>> IWANT = slice(20,31) 
    >>> record[IWANT]
    'I want this'
"""

"""Examples:
results_header = r'    Name                    Year School                  Finals  Points Alternate'
other_header = r'  Pl Athlete                 Yr   #  Team                      Score       Time  Avg. Mile    Avg. kM'
other_layout = r'  14 OWENS, Maddie           8  2744 Marietta High School         14   21:07.29     6:47.5     4:13.5'
# ======================================================================================================
#   Pl Athlete                 Yr   #  Team                      Score       Time  Avg. Mile    Avg. kM
# ======================================================================================================
#    1 JONES, Maggie           8  2686 Landmark Christian S              12:25.11     6:40.6     4:08.4
#    2 HARTMAN, Janet          FR 3168 Rome High School              1   13:08.57     7:04.0     4:22.9
"""