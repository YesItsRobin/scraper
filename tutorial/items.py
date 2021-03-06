# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import csv

#the parser class handles the aquisition of the data
class ParserClass():
    def __init__(self, paths, urlBuild,filen):
        self.paths = paths
        self.urlBuild = urlBuild
        self.page = 1

        self.file = open(filen, "w",newline="")
        self.writer=csv.writer(self.file)
        self.writer.writerow(["item", "recommended1", "recommended2", "recommended3","recommended4","recommended5"])

    async def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        print(links)
        for link in links[0]:                                #for every link
            print("--------------------------------------"+link)
            yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)
        
        if self.getPage()<5:                                                  #bol.com has (about) 25 pages in this category, just scraping the first 3 for faster testing
            self.page+=1                                                       #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            print('-----------------------now on to page: '+str(self.getPage())+'-----------------------')
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
        else:
            print('-----------------------done scraping-----------------------')

    async def parse_single(self, response):
        #try:
        recommended1=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(0)).get()
        recommended2=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(1)).get()
        recommended3=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(2)).get()
        recommended4=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(3)).get()
        recommended5=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(4)).get()
        data=[response.url,recommended1,recommended2,recommended3,recommended4,recommended5]
        #except:
        '''
            try:
                recommended1=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(0)).get()
                recommended2=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(1)).get()
                recommended3=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(2)).get()
                recommended4=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(3)).get()
                data=[response.url,recommended1,recommended2,recommended3,recommended4]
            except:
                try:
                    recommended1=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(0)).get()
                    recommended2=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(1)).get()
                    recommended3=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(2)).get()
                    data=[response.url,recommended1,recommended2,recommended3]
                except:
                    try:
                        recommended1=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(0)).get()
                        recommended2=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(1)).get()
                        data=[response.url,recommended1,recommended2]
                    except:
                        try:
                            recommended1=  self.getUrlBuild(2)+response.xpath(self.getSinglePath(0)).get()
                            data=[response.url,recommended1]
                        except:
                            data=[response.url]
                            '''
        self.write(data)
        print(data)
        print('\n\n')
            
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