from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import time
import random



def forum_topic_fetch(user_agent):
    """
      This funciton will fetch the catagories in the Naturally Curly forum page

      Keyword arguments:
      user_agent -- Using a different user agent than the default python one keeps the user from being kicked out by the website
    """
    #Make a get request to retrieve the page
    html_page = requests.get('https://curltalk.naturallycurly.com/', headers = {'User-Agent': user_agent} )
    soup = BeautifulSoup(html_page.content, 'html.parser')
    link_list_forum_top = []
    for link in soup.find_all('a'):
    link_list_forum_top.append(link.get('href'))
    categories = [s for s in link_list_forum_top if (("categories" in s) and ('https' in s))]
    return categories


def signature_fetch(categories, index_of_category_list, user_agent, start_range=0, finish_range=100):
    """
      This funciton will fetch the signatures from a forum topic

      Keyword arguments:
      catagories -- the list of category urls with no page number on them
      index_of_category_list -- which url in the list is deisred to be scraped
      user_agent -- using a different user agent than the default python one keeps the user from being kicked out by the website
      start_range -- default to start at page zero, but can be set to a different page number as it might need to be run a few times in approximatly 100 page increments
      finish_range -- default number of pages to stop scraping at, but this might need to be adjusted for very large or small number of pages on each topic url
    """
    # Get a list of specific discussion urls
    link_listdiscussion = []
    for i in range(start_range, finish_range):
        url = f'{categories[index_of_category_list]}/p{i}'
        html_page = requests.get(url, headers = {'User-Agent': user_agent} )

        # Check status code
        status = html_page.status_code
        if status != 200:
            print(f'Error improper response code. Code is {status}')

        # Pass the page contents to beautiful soup for parsing
        soup = BeautifulSoup(html_page.content, 'html.parser')
        # Create a list of discussions on each forum topic page
        for link in soup.find_all('a'):
            link_listdiscussion.append(link.get('href'))
            topics = [s for s in link_listdiscussion if (("/discussion" in s) and ('https' in s))]

    # Lets the user see the function is working should take a few minutes to get a result here depending on the range of pages looped through
    print(len(topics))

    # Loop through all the topics found for each catagory
    list_for_mongo = []
    count = 1
    for topic in topics:
        url2 = topic
        html_page2 = requests.get(url2, headers = {'User-Agent': user_agent} )

        # Check status code
        if status != 200:
            print(f'Error improper response code. Code is {status}')

        soup2 = BeautifulSoup(html_page2.content, 'html.parser')
        signatures = soup2.find_all('div', class_="Signature UserSignature userContent")

        for i in range(0,len(signatures)):
            sig = {}
            sig['signature'] = soup2.find_all('div', class_="Signature UserSignature userContent")[i].get_text()
            list_for_mongo.append(sig)
        count += 1

    return list_for_mongo
