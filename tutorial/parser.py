import scrapy

class Parser():
    def __init__(self, start, paths, urlBuild):
        self.paths = paths
        self.urlBuild = urlBuild
        self.page = 1
        self.allLinks = []
        self.allTitles = []
        self.allISBNs = []
        scrapy.Request(start, self.parse_all)
        for link in self.getAllLinks:
            scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)
        
        
    def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        print("--------------------------next page----------------------------")    #just for the user to know what is happening in the terminal
        for link in links[0]:                                #for every link
            self.getallLinks().append(link)
            #add the link to the total list
        if self.getPage()<=25:                                                    #bol.com only has 25 pages in this category 
            page+=1                                                     #increase the page number
            url= self.getUrlBuild(0)+str(self.getPage())+self.getUrlBuild(1)   #create the link for the next page
            yield scrapy.Request(url, self.parse_all)   #send the request to the parse function again
            
    
    def parse_single(self, response):
        title = [response.xpath(self.getSinglePath(0)).get()]
        isbn  = [response.xpath(self.getSinglePath(1)).get()]
        author= [response.xpath(self.getSinglePath(2)).get()]
        self.getallTitles().append(title)
        self.getallISBNs().append(isbn)
        self.getallAuthors().append(author)

    def getResponse(self):
        return self.response
    def getMainPath(self):
        return self.path[0]
    def getSinglePath(self,nr):
        return self.path[1][nr]
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