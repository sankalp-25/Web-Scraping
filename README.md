# Web-Scraping
This application is in scraping.py.
The data is fetched from "https://www.theverge.com/" using the python library known as Beautiful soup.
The parameters that are used from the data scraped were url, author, date, headline.
After scraping/fetching data, a .csv(comma seperated value) file is created with date as its name and in the format "DDMMYYYY_verge.csv".

Comments are written above the code scraping.py in a user understandable language.

The same data is also uploaded to the sqlite database with
1. Id as its primary key, which is unique for every article with no duplicates in it.
2. URL of the article
3. Headline of the article
4. Author of the article
5. Date on which the article was published

How to run :
python Scraping.py
