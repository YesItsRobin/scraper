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
        self.currLink = ''


        self.file = open(filen, "w")        #creates a csv file, if it doesn't exist yet
        self.writer=csv.writer(self.file)   #creates a writer object, this can be called to write rows in the file
        self.writer.writerow(["link", "rec1", "rec2", "etc...."])   #write the header
        self.temp=0                         #can be printed to check how many books are scraped
        
    async def parse_all(self,response):
        links   = [response.xpath(self.getMainPath()).getall()]     #get all the links of this page
        for link in links[0]:                                       #for every link(book) on the page
            self.putCurrLink(link)
            yield scrapy.Request(self.getUrlBuild(2)+link, self.parse_single)   #scrape the individual book page

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
        Fields=['recommendation 1','recommendation 2','recommendation 3','recommendation 4','recommendation 5',]
        filename="recommendations.csv"
        dataUrlScrapped=[]
        dataUrl=[]
        recommend=[response.xpath('//*[@id="mainContent"]/div/div[1]/div[5]/div[2]/div[2]/ul/li[1]/div/div[2]/a/@href').get(),
        response.xpath('//*[@id="mainContent"]/div/div[1]/div[5]/div[2]/div[2]/ul/li[2]/div/div[2]/a/@href').get(),
        response.xpath('//*[@id="mainContent"]/div/div[1]/div[5]/div[2]/div[2]/ul/li[3]/div/div[2]/a/@href').get(),
        response.xpath('//*[@id="mainContent"]/div/div[1]/div[5]/div[2]/div[2]/ul/li[4]/div/div[2]/a/@href').get(),
        response.xpath('//*[@id="mainContent"]/div/div[1]/div[5]/div[2]/div[2]/ul/li[5]/div/div[2]/a/@href').get()]

        print("Check the recommended items__________________________________________")#the links work
        for rec in recommend:
            print("The rec is "+rec)
            dataUrlScrapped.append(rec)# this works
    
        dataUrl.append(dataUrlScrapped)


        print(dataUrl)
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(Fields)
            csvwriter.writerows(dataUrl)




        #rec2
        #rec3
        #etc
        #data=[self.getCurrLink(),rec1,rec2,rec3,...,etc]

        #self.getWriter().writerow(data)
        self.temp+=1
            
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
    # def writte_csv(self,list):
    #     self.list=[]
    #     Fields = ['recommendation 1', 'recommendation 2', 'recommendation 3', 'recommendation 4', 'recommendation 5', ]
    #     filename = "recommendations.csv"
    #
    #     with open(filename, 'w') as csvfile:
    #         csvwriter = csv.writer(csvfile)
    #         csvwriter.writerow(Fields)
    #         csvwriter.writerows(list)