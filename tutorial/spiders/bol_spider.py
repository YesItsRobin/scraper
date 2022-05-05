from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess

#if any outside class is made, put it in items and import it like this here
from tutorial.items import ParserClass

#to run: scrapy runspider bol_spider.py

class BolSpider(scrapy.Spider):
    name = "bol" #the name that the spider will be called

    def start_requests(self):   #on startup, the spider will start here
        yield scrapy.Request(start, bolParser.parse_all) #send out the first request, the code leaves this class immediately

process = CrawlerProcess(settings={      #Some settings for the crawler
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

start='https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=1&12194=10-20'
paths= ['//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/@href',['---!!!put a list of Xpaths to reccomended books here!!!---']] 
urlBuild=['https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=','&12194=10-20','https://www.bol.com']
#this is information specific to the bol.com website

bolParser = ParserClass(paths,urlBuild,"bol.csv")
#creates a parser object, go to items.py to see/edit the parser class

process.crawl(BolSpider)    #puts the spider in the crawler
process.start() #Runs the spider, the script will block here until the crawling is finished
print('-----------------------done-----------------------\n\n\n\n\n\n\n\n') #this is for the user to know where the spider finishes
bolParser.file.close() #closes the csv file

#Code for mathematical part can be added here