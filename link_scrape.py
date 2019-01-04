#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import csv


source = requests.get('https://www.kenyaplex.com/business-directory/').text
links_list = []

csv_file = open('link_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)

# function to get links from any page
def getLinksPage(the_source,the_links_list):

    the_soup = BeautifulSoup(the_source, 'lxml')

    searchbox_div = the_soup.find('div', class_='searchbox')
    looper = searchbox_div

    for x in range(10):
        looped = looper.find_next_sibling()

        for d in  looper.find_all('div', class_='c-detail'):
            the_links_list.append(d.a['href'])
            csv_writer.writerow([d.a['href']])
            print(len(the_links_list))
            
        looper = looped

    return

# get first page links
getLinksPage(source, links_list)

# get link from all other pages  
links = 30
pages = 4
# pages = 3176

for i in range(pages):
    url = 'https://www.kenyaplex.com/business-directory/?start=' + str(links)
    source = requests.get(url).text
    
    getLinksPage(source, links_list)

    # print(pages)

    links+=30

print(len(links_list))
