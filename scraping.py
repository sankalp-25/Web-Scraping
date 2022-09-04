# Import module
import sqlite3

import requests
from bs4 import BeautifulSoup
import csv

URL="https://www.theverge.com/"
req=requests.get(URL)
site=BeautifulSoup(req.content,"html5lib")

#prettify is used to make the html code intented and in user understandable form
#print(site.prettify())

# Connecting to sqlite
conn = sqlite3.connect('sql_lite/ScrapeTables.db')
 
# Creating a cursor object
cursor = conn.cursor()

#This list is to get the titles that are already present in the database
#so that we can avoid the duplicates(urls can also be taken but the urls are changing, they are not same)
titles=[]

#Creating table
try:
    table ="""CREATE TABLE Scraping(ID INTEGER PRIMARY KEY AUTOINCREMENT, URL VARCHAR(300), HEADLINE VARCHAR(200), AUTHOR VARCHAR(30), DATE CHAR(10));"""
    cursor.execute(table)
except:
    titles=cursor.execute('''SELECT HEADLINE FROM Scraping''')
    pass

#getting the part of the verge.com's html where all the articles are present
# here all articles are present under <main></main> tag and the id was 'content'
details=[]
articles=site.find('main', attrs={'id':'content'})

#here we are iterating through all articles one by one.
#for each article there is a <div></div> tag and with a class c-entry-box--compact__body
#crating a dictionary for every article and appending the details into the list details(line 46, line 61)
#Authors for every article were in different tag inside the outer div tag, so iterating it each time and getting author name(line 54)
#The time tag was in some articles and in some articles there were no time tag, for that "N/A" is given(line 56)
i=0
for article in articles.findAll('div', attrs ={'class' : 'c-entry-box--compact__body'}):
    detail={}
    if((article.h2.text,) in titles):
        i=i+1
        continue
    else:
        detail['id']=i
        detail['url']=article.a['href']
        detail['headline']=article.h2.text
        l=articles.findAll("span",attrs={'class':'c-byline__author-name'})
        detail['author']=l[i].text
        if(article.time == None):
            detail['date']="N/A"
        else:
            p=article.time['datetime']
            detail['date']=p[:10] # because we only need date and not time
        details.append(detail)
        i=i+1

#here we are converting the date into a list ['DD','MM','YYYY]
#because the date we will be getting is in the format YYYY-MM-DD
kl=[]
for i in details:
    for j,k in i.items():
        if(j=='date' and k!='N/A'):
            kl=k.split('-')
            kl=kl[::-1]
            break
    if(len(kl)):
        break

#here converting the list ['DD','MM','YYYY] into a string DDMMYYYY 
ks=""
for i in kl:
    ks=ks+i

#creating the .csv file name in the DDMMYYYY_verge order
file_name=ks+'_verge.csv'

#here adding values to the DDMMYYYY_verge.csv file
with open(file_name, 'w', newline='') as f:
    w = csv.DictWriter(f,['id','url','headline','author','date'])
    w.writeheader()
    for detail in details:
        w.writerow(detail)

#inserting the data into the database
for x in details:
    cursor.execute('INSERT INTO scraping(url,headline,author,date) VALUES (?,?,?,?)',(x['url'],x['headline'],x['author'],x['date']))
 
# Commit
conn.commit()
 
# Closing 
conn.close()
