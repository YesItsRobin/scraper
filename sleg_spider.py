import scrapy
import time
from scrapy.crawler import CrawlerProcess
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
        self.allTitles = []
        self.allISBNs = []
        self.allAuthors = []

        Tfile = open("deslegteTitles.txt", "w")
        Ifile = open("deslegteISBNs.txt", "w")
        Afile = open("deslegteAutors.txt", "w")
        Tfile.close()
        Ifile.close()
        Afile.close()

        self.index=0
        
    def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                #for every link
            self.addLink(link)
            #add the link to the total list

        #TO-DO/HELP
        #Automate the ammount of pages possible, not hard

        if self.getPage()<16:                                                  #bol.com only has 25 pages in this category 
            self.page+=1                                                       #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            print('-----------------------done scraping booklist-----------------------')
            print('-----------------------now on to the individual books:-----------------------')
            yield scrapy.Request(self.getUrlBuild(2)+self.getallLinks()[0], self.parse_single)
       
            #TO-DO/HELP
            #for some reason it doesn't want to do the yield in the for loop before it ends this whole function so for now it's written in the files
    
    def parse_single(self, response):
        title=response.xpath(self.getSinglePath(0)).get()
        self.addTitle(title)
        isbn=response.xpath(self.getSinglePath(1)).get()
        self.addISBN(isbn)
        author=response.xpath(self.getSinglePath(2)).get()
        self.addAuthor(author)
        time.sleep(1)

        if self.getIndex()+1<=len(self.getallLinks()):
            self.addIndex()
            link=self.getallLinks()[self.getIndex()]
            yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)
        else:
            self.showResults()        

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

start='https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=1&sc=popularity&so=desc'
paths= ['/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/@href',['//*[@id="book-overview"]/h1/text()','//*[@id="book-specifications"]/ul/li[3]/div[2]/text()','//*[@id="book-specifications"]/ul/li[1]/div[2]/a[1]/text()']]
urlBuild=['https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=','','https://www.deslegte.com/']
bolParser = ParserClass(start,paths,urlBuild)

process.crawl(SlegSpider)
process.start() # the script will block here until the crawling is finished

print("BIG DONEZO")
showResults(bolParser)