import scrapy
from parser import Parser

#the imfamous bol spider
class BolSpider(scrapy.Spider):
    name = "bol" #the name that the spider will be called in the terminal
    #scrapy crawl bol

    def start_requests(self):   #on startup, the spider will start here
        start='https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=1&12194=10-20'
        paths= ['//*[@id="js_items_content"]/li/div[2]/div/div[1]/a/@href',['//*[@id="mainContent"]/div/div[1]/div[4]/h1/span[1]/text()','//*[@id="mainContent"]/div/div[1]/div[5]/div[1]/div[1]/div/div/ul/li[3]/text()','//*[@id="mainContent"]/div/div[1]/div[5]/div[1]/div[1]/div/div/div/div/a/text()']]
        urlBuild=['https://www.bol.com/nl/nl/l/engelse-boeken-over-voeding/41026/8292/?page=','&12194=10-20','https://www.bol.com/']
        
        bolParser = Parser(start,paths,urlBuild)
        print(bolParser.getallTitles())
        print(bolParser.getallAuthors())
        print(bolParser.getallISBNs())