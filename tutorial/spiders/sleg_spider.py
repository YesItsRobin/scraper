import scrapy
import csv
from scrapy.crawler import CrawlerProcess


#to run: scrapy runspider sleg_spider.py

#the imfamous DeSlegte spider
class SlegSpider(scrapy.Spider):
    name = "sleg" #the name that the spider will be called in the terminal

    def start_requests(self):   #on startup, the spider will start here
        yield scrapy.Request(start, bolParser.parse_all)

class ParserClass():
    def __init__(self, start, paths, urlBuild):
        self.paths = paths
        self.urlBuild = urlBuild
        self.page = 1
        self.allLinks = []

        self.file = open("sleg.csv", "w")
        self.writer=csv.writer(self.file)
        self.writer.writerow(["ISBN","Title","Author"])

        self.index=0
        
    async def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                #for every link
            self.addLink(link)
            #add the link to the total list

        #TO-DO/HELP
        #Automate the ammount of pages possible, prob not hard

        if self.getPage()<3:                                                  #deslegde only has 16 pages in this category 
            self.page+=1                                                       #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            print('-----------------------done scraping booklist-----------------------')
            print('-----------------------now on to the individual books:-----------------------')
            for link in self.getallLinks():
                yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)
            #yield scrapy.Request(self.getUrlBuild(2)+self.getallLinks()[0], self.parse_single)
       

    async def parse_single(self, response):
        isbn=  response.xpath(self.getSinglePath(1)).get()
        title=  response.xpath(self.getSinglePath(0)).get()
        author=  response.xpath(self.getSinglePath(2)).get()
        data=[isbn,title,author]

        self.getWriter().writerow(data)

        if self.getIndex()<len(self.getallLinks()):
            self.addIndex()
            link=self.getallLinks()[self.getIndex()]
            yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)       
            
    def getResponse(self):
        return self.response
    def getMainPath(self):
        return self.paths[0]
    def getSinglePath(self,nr):
        return self.paths[1][nr]
    def getUrlBuild(self,nr):
        return self.urlBuild[nr]
    def getPage(self):
        return self.page
    def getallLinks(self):
        return self.allLinks
    def getIndex(self):
        return self.index
    def getWriter(self):
        return self.writer
    def addLink(self,link):
        self.allLinks.append(link)
    def addIndex(self):
        self.index+=1

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

start='https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=1&sc=popularity&so=desc'
paths= ['/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/@href',['//*[@id="book-overview"]/h1/text()','//*[@id="book-specifications"]/ul/li[3]/div[2]/text()','//*[@id="book-specifications"]/ul/li[1]/div[2]/a[1]/text()']]
urlBuild=['https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=','','https://www.deslegte.com/']
bolParser = ParserClass(start,paths,urlBuild)

bolParser = ParserClass(start,paths,urlBuild)

process.crawl(SlegSpider)
process.start() # the script will block here until the crawling is finished

bolParser.file.close()