#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 09:34:47 2018

@author: mam

This program first makes a list of article links and then follows those to 
get the related content.
"""

from newspaper import Article
from classtools import AttrDisplay
from googleapiclient.discovery import build

import shelve
import json
import pandas as pd
import csv
import time


"""make a list of links for all the articles that have the keywords from a 
custom google search. It then follows each link and gets the author, date, and
text from the article, returning it as a python db.

TO USE: Set newspapers and word list at the bottom.
"""

wordlist = ['gun', 'firearm', 'AR15', 'weapon', 'shot', 'rifle']

"""Make a Google Custom Search for each newspaper. Find the CSE ID under 
Basics > Details > Search Engine ID
"""


#"Conservative"
#FoxNews
#paper = 'fox'
#custom_search_id = 'SECRET KEY'

##Wall Street Journal
#paper = 'wsj'
#custom_search_id = 'SECRET KEY'

##Breitbart
#paper = 'breitbart'
#custom_search_id = 'SECRET KEY'

##InfoWars
#paper='inforwars'
#custom_search_id = 'SECRET KEY'

##The Blaze
#paper = 'blaze'
#custom_search_id = 'SECRET KEY'


# "Liberal"
##NYTimes
#paper = 'nyt'
#custom_search_id = 'SECRET KEY'

##NPR
#paper='npr'
#custom_search_id = 'SECRET KEY'

##HuffingtonPost
#paper='huffpo'
#custom_search_id = 'SECRET KEY'

##The Nation
paper='nation'
custom_search_id = 'SECRET KEY

#MSNBC
#paper='msnbc'
#custom_search_id = '010452994600902477721:qeubtpqw868'

cses = {'msnbc': '010452994600902477721:qeubtpqw868', 
        'nation':'010452994600902477721:z1ay996qaji', 
       'huffpo':'010452994600902477721:e2pfkbhxyao', 
       'npr':'010452994600902477721:wjpsk4ndijs', 
       'nyt':'010452994600902477721:_xacvksvdiy', 
       'blaze': '010452994600902477721:hc9rksv3eos',
       'infowars':'010452994600902477721:qxbs3slzoje', 
       'breitbart':'010452994600902477721:jnqwe5bzppe', 
       'wsj':'010452994600902477721:lg-xm4efonu',
       'fox': '010452994600902477721:lrogmxjaknk'}

papers=['fox', 'wsj', 'breitbart', 'infowars', 'blaze', 'nyt', 'npr', 'huffpo', 'nation', 'msnbc']


def getService():
    service = build("customsearch", "v1",
            developerKey="AIzaSyC3bsWJ5I1dcA5Dqj3bVTTWtZo96lYwxvw")
    return service

def pagesearch(paper, engineid, wordlist):
    pageLimit = 10
    service = getService()
    startIndex = 1
    response = []
    for nPage in range(0, pageLimit):
        time.sleep(.001)
        for word in wordlist:
            response.append(service.cse().list(
                q=word, #Search words
                cx=engineid,  #CSE Key
                #lr='lang_pt', #Search language
                start=startIndex
            ).execute())
            startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")
    with open('newsLinkLists/'+paper+'data.json', 'w') as outfile:
        json.dump(response, outfile)

    outfile.close()

    data = json.load(open('newsLinkLists/'+paper+'data.json'))
    links=[]
    
    for obj in data:
        embedded = obj['items']
        for item in embedded:
            mylink = item['link']
            if mylink not in links:
                links.append(mylink)
            else:
                pass
            
    return links

class SavedArticles(AttrDisplay):
    def __init__(self, artid, paper, author, date, link, text):
        self.artid = artid
        self.paper = paper
        self.author = author
        self.date = date
        self.link = link
        self.text = text
    def wordCount(text):
        pass
    def keyWordCount(text):
        pass


def paperdb(paper, links):
    #use the results of the json file and find only the links.
    csvfile = open(paper+'.csv', 'w')
    w = csv.writer(csvfile)
    #make an empty list to check that it finished
    artids = []
    #Use the newspaper module to parse the articles
    for url in links:
        try:
            article = Article(url)
            
            article.download()
            article.parse()
            
            author = article.authors
            text = article.text
            date = article.publish_date
            
            artid = (paper+ str(links.index(url)))
            w.writerow([artid, paper, author, date, url, text])
            
            art = SavedArticles(artid, paper, author, date, url, text)
            artids.append(art.artid)

        except:
            pass
    return artids

        
#for paper in papers:
#    links = pagesearch(custom_search_id, wordlist, paper)
#    artids = paperdb(links, paper)
#    print(paper, len(artids), 'done')

    
#links = pagesearch(custom_search_id, wordlist, 'nation')
data = json.load(open('newsLinkLists/'+'nation'+'data.json'))
links=[]
for obj in data:
    embedded = obj['items']
    for item in embedded:
        mylink = item['link']
        if mylink not in links:
            links.append(mylink)
        else:
            pass
artids = paperdb(paper, links)
print(paper, len(artids), 'done')

    
