import scrapy
import time
from scrapy.crawler import CrawlerProcess

#to run: scrapy runspider bol_spider.py

class BolSpider(scrapy.Spider):
    name = "bol" #the name that the spider will be called in the terminal
    #scrapy crawl bol

    def start_requests(self):   #on startup, the spider will start here
        yield scrapy.Request(start, bolParser.parse_all)

class ParserClass():
    def __init__(self, start, paths, urlBuild):
        self.paths = paths
        self.urlBuild = urlBuild
        self.page = 1
        self.allLinks = []
        self.allTitles = []
        self.allISBNs = []
        self.allAuthors = []

        Tfile = open("bolTitles.txt", "w")
        Ifile = open("bolISBNs.txt", "w")
        Afile = open("bolAutors.txt", "w")
        Tfile.close()
        Ifile.close()
        Afile.close()

        self.index=0
        
    async def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                #for every link
            self.addLink(link)
            #add the link to the total list

        #TO-DO/HELP
        #Automate the ammount of pages possible, prob not hard

        if self.getPage()<5:                                                  #deslegde only has 16 pages in this category 
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
        title=  response.xpath(self.getSinglePath(0)).get()
        self.addTitle(title)
        isbn=  response.xpath(self.getSinglePath(1)).get()
        self.addISBN(isbn)
        author=  response.xpath(self.getSinglePath(2)).get()
        self.addAuthor(author)
        #time.sleep(1)

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
    def getallTitles(self): 
        return self.allTitles
    def getallISBNs(self):
        return self.allISBNs
    def getallAuthors(self):
        return self.allAuthors
    def getIndex(self):
        return self.index
    def addTitle(self,title):
        self.allTitles.append(title)
    def addISBN(self,isbn):
        self.allISBNs.append(isbn)
    def addAuthor(self,author):
        self.allAuthors.append(author)
    def addLink(self,link):
        self.allLinks.append(link)
    def addIndex(self):
        self.index+=1

def showResults(bolParser):
        print('-----------------------done scraping individual books-----------------------\n\n\n\n\n\n\n\n\n\n')
        print('-----------------------All links:-----------------------')
        print(bolParser.getallLinks())
        print('total of '+str(len(bolParser.getallLinks()))+' links')
        print('-----------------------All titles:-----------------------')
        print(bolParser.getallTitles())
        print('total of '+str(len(bolParser.getallTitles()))+' titles')
        print('-----------------------All ISBNs:-----------------------')
        print(bolParser.getallISBNs())            
        print('total of '+str(len(bolParser.getallISBNs()))+' ISBNs')
        print('-----------------------All authors:-----------------------')
        print(bolParser.getallAuthors())
        print('total of '+str(len(bolParser.getallAuthors()))+' authors')
        print('-----------------------done scraping-----------------------')

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

start='https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=1&12194=10-20'
paths= ['//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/@href',['//*[@id="mainContent"]/div/div[1]/div[4]/h1/span[1]/text()','//*[@id="mainContent"]/div/div[1]/div[5]/div[1]/div[1]/div/div/ul/li[3]/text()','//*[@id="mainContent"]/div/div[1]/div[5]/div[1]/div[1]/div/div/div/div/a/text()']]
urlBuild=['https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=','&12194=10-20','https://www.bol.com']
        
bolParser = ParserClass(start,paths,urlBuild)

process.crawl(BolSpider)
process.start() # the script will block here until the crawling is finished

showResults(bolParser)
Tfile = open("bolTitles.txt", "a")
Ifile = open("bolISBNs.txt", "a")
Afile = open("bolAutors.txt", "a")

for i in range (len(bolParser.getallTitles())):
    Tfile.write(bolParser.getallTitles[i]+',')
    Ifile.write(bolParser.getallISBNs[i]+',')
    Afile.write(bolParser.getallAuthors[i]+',')

Tfile.close()
Ifile.close()
Afile.close()