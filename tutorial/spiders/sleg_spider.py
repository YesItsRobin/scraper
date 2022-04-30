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
        links   = [response.xpath('/html/body/div[2]/div[2]/div/div[3]/ul/li/div/div/div[2]/h3/a/@href').getall()]           #get all the links of this page

        print("--------------------------next page----------------------------")    #just for the user to know what is happening in the terminal
        print(len(links[0]))
        for i in range (len(links[0])):                                #for every title
            total.append(links[0][i])                    #add the title and the link to the total list. Will give error now, because more titles then links
        
        if page<=15:                                                    #bol.com only has 25 pages in this category 
            page+=1                                                         #increase the page number
            url= 'https://www.deslegte.com/boeken/koken-reizen-vrije-tijd/koken/engels/10-20-euro/?p='+str(page)    #create the link for the next page
            yield scrapy.Request(url, self.parse)   #send the request to the parse function again
        else:
            print(total)                            #print the total list when the spider has finished, just for show now
            