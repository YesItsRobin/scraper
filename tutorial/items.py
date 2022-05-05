# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

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
        if self.getPage()<3:                                                  #bol.com has (about) 25 pages in this category, just scraping the first 3 for faster testing
            self.page+=1                                                       #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            print('-----------------------now on to page: '+str(self.getPage())+'-----------------------')
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            print('-----------------------done scraping-----------------------')

    async def parse_single(self, response):
        #recommended1=  response.xpath(self.getSinglePath(2)).get()
        #rec2
        #rec3
        #etc
        #data=[self.getCurrLink(),rec1,rec2,rec3,...,etc]

        #self.getWriter().writerow(data)
        self.temp+=1
        #pass    #remove if you add any code to this method
            
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