#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import csv
import time

api_key = 'AIzaSyD6jl8JDlhCOLhGupqg9NYqFV6LY3xS_f8'

csv_file = open('directory_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['Business Name',	'Description',	'Business Segment',	'Telephone Main',	'Cell ', 'Email', 'Website', 'City/Town', 'Business Address', 'map_lat',	'map_long',	'logoURL',
'Locality',	'County','Street Name',	'Building',	'Twitter',	'Facebook', 	'Linkedin',	'Youtube',	'Instagram',	'Claimed Statues',	'Gallery',	'Tagline',	'Price Statues',	'Price From',	'Price to',	'Price Plan',	'Business Hours',	'Features'])

def checker(a_url):
    page = ''
    while page == '':
        try:
            page = requests.get(a_url)
            getDataFromPage(page)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

def getDataFromPage(the_page):
    
    source = the_page.text

    soup = BeautifulSoup(source, 'lxml')

    title= ''
    logoURL= ''
    address= ''
    city= ''
    phone1= ''
    phone2= ''
    email= ''
    website= ''
    category= ''
    description= ''
    lat= ''
    lng= ''

    if soup.find('h1', class_='full-title') is not None:
        title = soup.find('h1', class_='full-title').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblLogo')is not None:
        logoURL = soup.find('span',id='ContentPlaceHolder1_lblLogo').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblAddress') is not None:
        address = soup.find('span',id='ContentPlaceHolder1_lblAddress').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblCity') is not None:
        city = soup.find('span',id='ContentPlaceHolder1_lblCity').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblPhoneNumber1') is not None:
        phone1 = soup.find('span',id='ContentPlaceHolder1_lblPhoneNumber1').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblPhoneNumber2') is not None:
        phone2 = soup.find('span',id='ContentPlaceHolder1_lblPhoneNumber2').text .rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblEmail') is not None:
        email = soup.find('span',id='ContentPlaceHolder1_lblEmail').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblHomePage') is not None:
        website = soup.find('span',id='ContentPlaceHolder1_lblHomePage').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblCategory') is not None:
        category = soup.find('span',id='ContentPlaceHolder1_lblCategory').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblDescription') is not None:
        description = soup.find('span',id='ContentPlaceHolder1_lblDescription').text.rstrip().strip()
    if soup.find('span',id='ContentPlaceHolder1_lblLogo').img is not None:
        lU = soup.find('span',id='ContentPlaceHolder1_lblLogo').img['src']
        l = lU.split('../')
        logoURL= 'https://www.kenyaplex.com/'+l[1]


    address_split = address.split(' ')
    address_split = '+'.join(address_split)

    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address_split+'&key='+api_key)

    resp_json_payload = response.json()
    lat = resp_json_payload['results'][0]['geometry']['location']['lat']
    lng = resp_json_payload['results'][0]['geometry']['location']['lng']
    
    the_row = [title,description,category,phone1,phone2,email,website,city,address,lat,lng,logoURL]
    csv_writer.writerow(the_row)

    print(the_row)
    return


with open('link_scrape.csv', 'rb') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print('Empty csv file')
            line_count += 1
        else:
            # getDataFromPage(row[0])
            checker(row[0])
            line_count += 1