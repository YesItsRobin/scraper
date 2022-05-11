from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess

#if any outside class is made, put it in items and import it like this here
from tutorial.items import ParserClass

#to run: scrapy runspider sleg_spider.py

class SlegSpider(scrapy.Spider):
    name = "sleg" #the name that the spider will be called

    def start_requests(self):   #on startup, the spider will start here
        yield scrapy.Request(start, slegParser.parse_all) #send out the first request, the code leaves this class immediately
        yield scrapy.Request(start, slegParser.parse_single())
process = CrawlerProcess(settings={      #Some settings for the crawler
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

start='https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=1&sc=popularity&so=desc'
paths= ['/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/@href','//*[@id="mainContent"]/div/div[1]/div[5]/div[2]/div[2]/ul/li[1]/div/div[2]/a/span']# first rec link added/ same for every
# get link href,
urlBuild=['https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=','','https://www.deslegte.com/']
#creates a parser object, go to items.py to see/edit the parser class

slegParser = ParserClass(paths,urlBuild,"sleg.csv")

process.crawl(slegParser)    #puts the spider in the crawler
process.start() #Runs the spider, the script will block here until the crawling is finished
print('-----------------------done-----------------------\n\n\n\n\n\n\n\n') #this is for the user to know where the spider finishes
slegParser.file.close() #closes the csv file

#Code for mathematical part can be added here