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
        self.currLink = ''

        self.file = open("bol.csv", "w")
        self.writer=csv.writer(self.file)
        self.writer.writerow(["link", "rec1", "rec2", "etc...."])

        self.temp=0
        
    async def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                #for every link
            self.putCurrLink(link)
            yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)

        #TO-DO/HELP
        #Automate the ammount of pages possible, prob not hard
        if self.getPage()<3:                                                  #deslegde has (about) 16 pages in this category, just scraping the first 3 for faster testing
            self.page+=1                                                       #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            print('-----------------------now on to page: '+str(self.getPage())+'-----------------------')
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            print('-----------------------done scraping-----------------------')

    async def parse_single(self, response):
        self.temp+=1
        #recommended1=  response.xpath(self.getSinglePath(2)).get()
        #rec2
        #rec3
        #etc
        #data=[self.getCurrLink(),rec1,rec2,rec3,...,etc]

        #self.getWriter().writerow(data)
            #remove if you add any code to this method
            
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
    def getCurrLink(self):
        return self.currLink
    def getWriter(self):
        return self.writer
    def addLink(self,link):
        self.allLinks.append(link)
    def putCurrLink(self,link):
        self.currLink=link

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
print('-----------------------done-----------------------')
print('\n\n\n\n\n\n\n\n\n\n')
print(bolParser.temp)
bolParser.file.close()