# -*- coding: utf-8 -*-
# This type of spiders is a crawling spider, where we give it a link and let it to scrape all relative links automatically on its own
# where the types of links to scrape can be specified using the rules objet below that'll contain some...rules :3

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'film_data'
    allowed_domains = ['www.imdb.com']

    def start_requests(self):
        genres = ['action' ,'adventure' , 'animation' , 'biography' , 'comedy' , 'crime' ,'documentary',
                  'drama' , 'family' , 'fantasy' , 'film-noir' , 'history' , 'horror' , 'music' , 'musical',
                  'mystery' , 'romance' , 'sci-fi', 'short-film' , 'sport' , 'superhere' , 'thriller' , 'war',
                  'western']
        yield scrapy.Request(url = 'https://www.imdb.com/search/title/?genres=action&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=facfbd0c-6f3d-4c05-9348-22eebd58852e&pf_rd_r=RM5G1P98V4E47ACFWDC3&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_1')


    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class = "lister-item mode-advanced"]'), callback='parse_item', follow=True),
        #here i assume each time an item is found, a response object is generated and used as an argument while calling the parse_item method
        Rule(LinkExtractor(restrict_xpaths="(//a[@class = 'lister-page-next next-page'])[2]"))
        #here apparently once it it clicks on the next page button or url in our case, it'll be redirected to the next page and starts automatically looking
        #for similar patterns using the first rule again; smfh
    )

    def parse_item(self, response):
        yield {
            'title' : response.xpath("//span[@class = 'lister-item-index unbold text-primary']/text()").get(),
            'year' : response.xpath("//span[@class = 'lister-item-year text-muted unbold']/text()").get(),
            'duration' : response.xpath("//span[@class = 'runtime']/text()").get(),
            'genre' : response.xpath("normalize-space(//span[@class = 'genre']/text())").get(),
            'meta_score' : response.xpath("normalize-space(//span[@class = 'metascore  mixed']/text())").get(),
            'description' : response.xpath("normalize-space(//p[@class = 'text-muted'])").get(),
            'directors/actors' : response.xpath("//p[contains(text() , 'Director')]/a/text()").get()
        }

