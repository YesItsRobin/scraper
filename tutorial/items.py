# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import csv

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ParserClass():
    def __init__(self, start, paths, urlBuild,filen):
        self.paths = paths
        self.urlBuild = urlBuild
        self.page = 1

        self.file = open(filen, "w")
        self.writer=csv.writer(self.file)
        self.writer.writerow(["item", "recommended1", "recommended2", "recommended3","recommended4","recommended5"])
        
    async def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                #for every link
            yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)

        if self.getPage()<3:                                                  #bol.com has (about) 25 pages in this category, just scraping the first 3 for faster testing
            self.page+=1                                                       #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            print('-----------------------now on to page: '+str(self.getPage())+'-----------------------')
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            print('-----------------------done scraping-----------------------')

    async def parse_single(self, response):
        recommended1=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(0)).get()
        recommended2=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(1)).get()
        recommended3=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(2)).get()
        recommended4=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(3)).get()
        recommended5=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(4)).get()
        data=[response.url,recommended1,recommended2,recommended3,recommended4,recommended5]
        self.write(data)
        print('\n\n\n\n\n\n')
        print(data)
        print('\n\n\n\n\n\n')
            
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
    def write(self,text):
        return self.writer.writerow(text)
    def addLink(self,link):
        self.allLinks.append(link)