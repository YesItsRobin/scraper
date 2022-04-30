import scrapy

#the imfamous bol spider
class BolSpider(scrapy.Spider):
    name = "bol" #the name that the spider will be called in the terminal
    #scrapy crawl bol

    def start_requests(self):   #on startup, the spider will start here
        start='https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=1&12194=10-20'
        paths= ['//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/@href',['//*[@id="mainContent"]/div/div[1]/div[4]/h1/span[1]/text()','//*[@id="mainContent"]/div/div[1]/div[5]/div[1]/div[1]/div/div/ul/li[3]/text()','//*[@id="mainContent"]/div/div[1]/div[5]/div[1]/div[1]/div/div/div/div/a/text()']]
        urlBuild=['https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=','&12194=10-20','https://www.bol.com']
        
        bolParser = ParserClass(start,paths,urlBuild)

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
    def addTitle(self,title):
        self.allTitles.append(title)
    def addISBN(self,isbn):
        self.allISBNs.append(isbn)
    def addAuthor(self,author):
        self.allAuthors.append(author)
        
    def parse_single(self, response):
        title = [response.xpath(self.getSinglePath(0)).get()]
        isbn  = [response.xpath(self.getSinglePath(1)).get()]
        author= [response.xpath(self.getSinglePath(2)).get()]
        self.addTitle(title)
        self.addISBN(isbn)
        self.addAuthor(author)
        
    def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                #for every link
            self.getallLinks().append(link)
            #add the link to the total list
        if self.getPage()<=5:                                                    #bol.com only has 25 pages in this category 
            self.page+=1                                                     #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            #for link in self.getallLinks():
            #    yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)
            #print('------------------done scraping------------------')
            print(self.getallLinks())
            #print(self.getallTitles())
            #print(self.getallAuthors())
            #print(self.getallISBNs())