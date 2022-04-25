from functools import total_ordering
import scrapy

#the imfamous bol spider
class BolSpider(scrapy.Spider):
    name = "bol" #the name that the spider will be called in the terminal

    def start_requests(self):   #on startup, the spider will start here
        global page, total      #declare the global variables
        total=[]                #initialize the global variables
        page=1                  #^

        url = 'https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=1&12194=10-20'  #the url that the spider will start with
        yield scrapy.Request(url, self.parse)   #send the request to the parse function

    #the parse function
    def parse(self, response):
        global page, total  #remember the global variables?

        titles  = [response.xpath('//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/text()').getall()]    #get all the titles of this page
        links   = [response.xpath('//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/@href').getall()]     #get all the links of this page
        ibsn    =[response.xpath('//*[@id="js_items_content"]/li[23]/div[2]/div/ul[2]/font/li/span/text()').getall()]
        print("The ibsn"+ibsn)
        print("--------------------------next page----------------------------")    #just for the user to know what is happening in the terminal
        for i in range (len(titles[0])):                                #for every title
            total.append([titles[0][i],ibsn[0][i]])
            #add the title and the link to the total list
        page+=1                                                         #increase the page number
        if page<=25:                                                    #bol.com only has 25 pages in this category
            url= 'https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page='+str(page)+'&12194=10-20'   #create the link for the next page
            yield scrapy.Request(url, self.parse)   #send the request to the parse function again
        else:
            print(total)                            #print the total list when the spider has finished, just for show now