from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from tutorial.items import ParserClass

#to run: scrapy runspider bol_spider.py

class BolSpider(scrapy.Spider):
    name = "bol" #the name that the spider will be called in the terminal
    #scrapy crawl bol

    def start_requests(self):   #on startup, the spider will start here
        yield scrapy.Request(start, bolParser.parse_all) #send out the first request, the code leaves this class immediately

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

start='https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=1&12194=10-20'
paths= ['//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/@href',['---!!!put a list of Xpaths to reccomended books here!!!---']] 
urlBuild=['https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=','&12194=10-20','https://www.bol.com']

bolParser = ParserClass(start,paths,urlBuild,"bol.csv")

process.crawl(BolSpider)
process.start() # the script will block here until the crawling is finished
print('-----------------------done-----------------------\n\n\n\n\n\n\n\n')
print(bolParser.temp)
bolParser.file.close()