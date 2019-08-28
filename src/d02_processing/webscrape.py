from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import time
import random



def forum_topic_fetch(user_agent,):
    """
      This funciton will fetch the catagories in the NAturally Curly forum page

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


link_listdiscussion = []
for i in range(0, 10):
    url = f'{categories[52]}/p{i}'
    print(url)
    user_agent =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    html_page = requests.get(url, headers = {'User-Agent': user_agent} ) #Make a get request to retrieve the page

    # Check status code for an appropriate response fromt the API
    status = html_page.status_code
    if status != 200:
        print(f'Error improper response code. Code is {status}')
        #break
    soup = BeautifulSoup(html_page.content, 'html.parser') #Pass the page contents to beautiful soup for parsing
    page1_of_discussion = []
    #time.sleep(random.randint(20,45))
    for link in soup.find_all('a'):
        link_listdiscussion.append(link.get('href'))
        topics = [s for s in link_listdiscussion if (("/discussion" in s) and ('https' in s))]

print(len(topics))
# Loop through all the topics found for each catagory
list_for_mongo = []
count = 1
for topic in topics:
    url2 = topic
    user_agent =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    html_page2 = requests.get(url2, headers = {'User-Agent': user_agent} )

    if status != 200:
        print(f'Error improper response code. Code is {status}')
        #break

    soup2 = BeautifulSoup(html_page2.content, 'html.parser')
    signatures = soup2.find_all('div', class_="Signature UserSignature userContent")

    for i in range(0,len(signatures)):
        sig = {}
        sig['signature'] = soup2.find_all('div', class_="Signature UserSignature userContent")[i].get_text()
        list_for_mongo.append(sig)
#     time.sleep(random.randint(1,5))
    print(count)
    count += 1
