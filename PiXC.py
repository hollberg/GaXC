"""PiXC.py - Paideia Cross Country
Given the "base" url of a cross-country race:
    1) Pull hyperlinks to the results of all EVENTS at that race
    2) Navigate to each results page, save copy of results to a *.csv file"""

import requests
from bs4 import BeautifulSoup
import config
import csv

links_list = []     # Stores links to all EVENTS
results_list = []   # Stores all individual results

for race, race_link in config.races.items():
    race_page = config.get_soup(race_link)
    results_table = race_page.find('table', {'class': 'meetResultsList'})

    if results_table != None:
        age_group_links = results_table.find_all('a')
        if age_group_links != None:
            for link in age_group_links:
                url = link.attrs['href']
                url = url.replace('auto', 'raw')
                if url[-1] == r'/':
                    url += 'raw'  # Ensure all links end with 'raw'
                links_list.append((race,link.text.strip(), 'http://ga.milesplit.com'+ url, ))

# print('***LINKS LIST***')
with open('event_links.csv', 'w', newline='') as csvfile:
    event_links_writer = csv.writer(csvfile, delimiter='|' )
    event_links_writer.writerow(['Meet', 'Event', 'Link'])
    for row in links_list:
        # print(row)
        event_links_writer.writerow(row)

# print('*** MEET RESULTS***')
for event in links_list:
    event_results = get_soup(event[2])
    event_data = event_results.find('div', {'id': 'meetResultsBody'})
    header_reached = False
    parse_type = ''

    if event_data == None:
        print(f'***No <pre> text at :{event}***')
        continue

    for i, row in enumerate(event_data.pre.text.split('\n')):
        if row.replace(' ', '').startswith('NameYearSchoolFinalsPoint'):
            parse_type = config.perfect_timing_parse
            header_reached = True
            header_row = i
        if row.replace(' ','').startswith('PlAthleteYr'):
            parse_type = config.fast_feet_parse
            header_reached = True
            header_row = i

        if header_reached and i > header_row+1:
            if row.strip() == '': #Then have hit last results record, exit loop
                break
            competitor = [row[value] for value in parse_type.values()]
            competitor.append(event[0])
            competitor.append(event[1])
            competitor.append(event[2])
            # print(competitor)
            results_list.append(competitor)

with open('results.csv', 'w', newline='') as csvfile:
    results_writer = csv.writer(csvfile, delimiter='|', )
    results_writer.writerow(config.headers)

    for result in results_list:
        results_writer.writerow(result)