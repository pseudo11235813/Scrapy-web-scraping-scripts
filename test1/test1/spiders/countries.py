# -*- coding: utf-8 -*-
import scrapy
import csv
 
class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info'] #this part here should never start with "https/http" NEVER EVER
    start_urls = ['http://www.worldometers.info/world-population/population-by-country/'] #the name of this variable must be the same otherwise the spider won't 
                                                                                           #work only if change this default behaviour


    def parse(self, response): #same note for the var name except that this is afunction so, the function name must remain the same
                               #as well when http request is sent a response object will be created and it'll contain the
                               #the HTML code for that website 
        data = response.xpath("//td/a")
        # print(data); here we get a set of selector objects
        # print(data.getall()); here we get the date of each selector object, both come in the same form, sequentially
    
        with open('countries.txt' , 'w') as file:
            writer = csv.writer(file)
            for en in data:
                name = en.xpath('.//text()').get()
                link = en.xpath('.//@href').get()
                # ab_link = f'https://www.worldometers.info{link}'
                # writer.writerow([str(name),str(link)])
                # yield scrapy.Request(url = ab_link)
                # ab_link = response.urljoin(link)

                yield response.follow(link , callback = self.parse_country , meta = {'country_name' : name}) #This callback attr is responsible for returning the response object to the 
                                                                            #added method, which is here 'parse_country()', which is basically the same thing
                                                                            #as calling the 'parse_country()' method using the response returned as an argument.
        
    def parse_country(self, response):
        country_name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class ='table table-striped table-bordered table-hover table-condensed table-list' ])[1]/tbody/tr")
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
        
            yield{
                'country_name' : country_name,
                'year' : year,
                'population' : population
            }