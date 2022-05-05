from __future__ import absolute_import
import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from tutorial.items import ParserClass

#to run: scrapy runspider sleg_spider.py

#the imfamous DeSlegte spider
class SlegSpider(scrapy.Spider):
    name = "sleg" #the name that the spider will be called

    def start_requests(self):   #on startup, the spider will start here
        yield scrapy.Request(start, bolParser.parse_all) #send out the first request, the code leaves this class immediately

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

start='https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=1&sc=popularity&so=desc'
paths= ['/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/@href',['---!!!put a list of Xpaths to reccomended books here!!!---']]
urlBuild=['https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=','','https://www.deslegte.com/']
bolParser = ParserClass(start,paths,urlBuild)

process.crawl(SlegSpider)
process.start() # the script will block here until the crawling is finished

print('-----------------------done-----------------------\n\n\n\n\n\n\n\n')
print(bolParser.temp)
bolParser.file.close()