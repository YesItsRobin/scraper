from functools import total_ordering
import scrapy

#the imfamous DeSlegte spider
class SlegSpider(scrapy.Spider):
    name = "sleg" #the name that the spider will be called in the terminal

    def start_requests(self):   #on startup, the spider will start here
        global page, total      #declare the global variables
        total=[]                #initialize the global variables
        page=1                  #^

        url = 'https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p=1&sc=popularity&so=desc'  #the url that the spider will start with
        yield scrapy.Request(url, self.parse)   #send the request to the parse function

    #the parse function
    def parse(self, response):
        global page, total  #remember the global variables?

        titles  = [response.xpath('/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/span/text()').getall()]     #get all the titles of this page
        links   = [response.xpath('/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/@href').getall()]           #get all the links of this page

        #// *[ @ id = "js_items_content"] / li[1] / div[2] / div / div[1] / a get the links from bol.com inspect
        #// *[ @ id = "mainContent"] / div / div[1] / div[5] / div[1] / div[1] / div / div / ul / font / li[3] ibsn
        print("--------------------------next page----------------------------")    #just for the user to know what is happening in the terminal
        print(len(titles[0]))   #there is a difference in titles and links, this is because some items have two titles. YET TO FIX
        print(len(links[0]))
        #for i in range (len(titles[0])):                                #for every title
        #    total.append([titles[0][i],links[0][i]])                    #add the title and the link to the total list. Will give error now, because more titles then links
        page+=1                                                         #increase the page number
        if page<=15:                                                    #bol.com only has 25 pages in this category 
            url= 'https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p='+str(page)    #create the link for the next page
            yield scrapy.Request(url, self.parse)   #send the request to the parse function again
        else:
            print(total)                            #print the total list when the spider has finished, just for show now