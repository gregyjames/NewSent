import urllib2
from bs4 import BeautifulSoup
from textblob import TextBlob 

#Analize the sentiments
def get_sentiment(title): 
    analysis = TextBlob(title) 
    sentiment_n = 0
    sentiment_t = ""

    if analysis.sentiment.polarity > 0: 
        sentiment_t = "positive"

    elif analysis.sentiment.polarity == 0: 
        sentiment_t = "neutral"
    else: 
        sentiment_t = "negative"
        
    sentiment_n = analysis.sentiment.polarity
    return sentiment_t, sentiment_n

avgSent = 0                             #Where will will keep the sum of the sentiments
keyword = "oil"                         #The google search term (format as such)
site = "bloomberg.com"                  #The site we are limiting the searches to
datarange = "y"                         #The date range of articles d:day, w:prev seven days, m: past month, y:past year
cr = "US"                               #Country 
num = 10                                #Number of articles to get from 1-99

#The google search url
url = "https://www.google.com/search?q=site:" + site + "+%22" + keyword+"%22&tbm=nws&source=lnt&num=" + str(num) + "&as_qdr=" + datarange + "&cr=country" + cr;

#Headers so google doesn't give us 403 forbidden
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#The request with the headers
req = urllib2.Request(url, headers=hdr)

#Get the text from the urllib request
html =urllib2.urlopen(req)
text = html.read()

#Parse the text as html
soup = BeautifulSoup(text, 'html.parser')

#Get the divs for all the article titles
mydivs = soup.findAll("div", {"class": "phYMDf nDgy9d"})

#Process each article title
for myString in mydivs:
    #get the inner html of the title div
    title = myString.text
    #Print the sentiment and the title
    sentiment_t,sentiment_n = get_sentiment(title)
    print title
    print sentiment_t
    print sentiment_n
    print "==============="
    #Add to avg sent
    avgSent += sentiment_n

#Calculate the average sentiment from all the articles
print "Average sentiment for term: " + str(avgSent/(len(mydivs) - 1))