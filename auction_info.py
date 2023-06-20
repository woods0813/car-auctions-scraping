import os
import requests
import numpy as np
from bs4 import BeautifulSoup
import random
import time

#scraping a car auction site
URL='https://www.renebates.com/'
referrer=r'https://zoom.us'
user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]
r=requests.get(URL,headers = {'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]})
soup=BeautifulSoup(r.content,'html5lib')
links=soup.find_all('a')
links=links[56:]

first_link=links[0]
first_url=first_link['href']
print(first_url)
r=requests.get(URL+first_url,headers = {'Referrer':URL,'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]})
soup=BeautifulSoup(r.content,'html5lib')
links=soup.find_all('a')

for link in links:
    href=link['href']
    if href.find('cat=all')!=-1:
        listing_url=href

r=requests.get(URL+listing_url,headers={'Referrer':URL+first_url,'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]})
soup=BeautifulSoup(r.content,'html5lib')
links=soup.find_all('a')
bids_links=[]
lots=[]

#searched through the href to find bids and lots
for link in links:
    href=link['href']
    if href.find('a_bids_2')!=-1:
        bids_links.append(href)
    if href.find('a_lot_2')!=-1:
        lots.append(href)
        
#find where in the html lot text that the lot starts
lots_links=[]
for i in range(len(lots)):
    lots_links_str=lots[i]
    lot_number_idx=lots_links_str.find('lot=')
    lot_number_inlink=lots_links_str[lot_number_idx+len('lot='):lot_number_idx+len('lot=')+5]
    print(lot_number_inlink)
    lots_links.append(lot_number_inlink)

lots_links_final=[]
for i in range(len(lots_links)):
    if i==0:
        lots_links_final.append(lots[i])
    if i>0 and lots_links[i]!=lots_links[i-1]:
        lots_links_final.append(lots[i])
lot_info=[]
lot_number=[]

#parse through the text to find lot info and lot number
for i in range(0,len(lots_links_final),1):
    r=requests.get(URL+lots_links_final[i],headers={'Referrer':URL+listing_url,'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]})
    soup=BeautifulSoup(r.content,'html5lib')
    text=str(soup.get_text(strip=True))
    starting_idx=text.find('Lot:')
    ending_idx=text.find('THIS  IS AN ABANDONED')
    lot_info.append(text[starting_idx+len('Lot: ')+12:ending_idx-len('Show Disclaimers')])
    lot_number.append(text[starting_idx+len('Lot: '):starting_idx+len('Lot: ')+12])


#parse through the text to find bids for the lot
bids=[]
for i in range(0,len(bids_links),1):
    r=requests.get(URL+bids_links[i],headers={'Referrer':URL+listing_url,'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]})
    soup=BeautifulSoup(r.content,'html5lib')
    text=str(soup.get_text())
    idx=text.find('Bidder')
    starting_idx=text.find('Bidder',idx+len('Bidder'),len(text))
    ending_idx=text.find('Note: Due to undisclosed')
    bids_for_lot=text[starting_idx:ending_idx-20]
    bids_for_lot_new='\t'+'\t'+'\t'+bids_for_lot
    bids_for_lot_new=bids_for_lot_new.replace('\t','')
    bids.append(bids_for_lot_new)

#write the information to a text file
with open('sample_auction_info.txt','w') as f:
    for i in range(len(bids)):
        f.write('Lot Number: ' +lot_number[i])
        f.write('\n')
        f.write('\n')
        f.write('Lot Info: ' +lot_info[i])
        f.write('\n')
        f.write('\n')
        f.write('Bids:'+'\n')
        f.write(bids[i])
        f.write('\n')
        f.write('\n')
        f.write('----------------------------------------------------------')
        f.write('\n')
        f.write('\n')

