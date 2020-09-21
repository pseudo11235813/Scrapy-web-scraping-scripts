# -*- coding: utf-8 -*-
import scrapy
import sys

class FilmIMDbCrawlerSpider(scrapy.Spider):
    name = 'imdb_crawler'
    allowed_domains = ['www.imdb.com']
    movies = []
    def start_requests(self):
        genres = ['action' ,'adventure' , 'animation' , 'biography' , 'comedy' , 'crime' ,'documentary',
                  'drama' , 'family' , 'fantasy' , 'film-noir' , 'history' , 'horror' , 'music' , 'musical',
                  'mystery' , 'romance' , 'sci-fi', 'short-film' , 'sport' , 'superhere' , 'thriller' , 'war',
                  'western']
        for genre in genres:
            yield scrapy.Request(url = f'https://www.imdb.com/search/title/?genres={genre}&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=facfbd0c-6f3d-4c05-9348-22eebd58852e&pf_rd_r=RM5G1P98V4E47ACFWDC3&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_1',
                             callback=self.parse)

    def parse(self, response):
        films = response.xpath('//div[@class = "lister-item mode-advanced"]')
        for film in films:
            if film.xpath(".//h3[@class = 'lister-item-header']/a/text()").get() in self.movies:
                break
            else:
                self.movies.append(film.xpath(".//h3[@class = 'lister-item-header']/a/text()").get())
                yield {
                    'title': film.xpath(".//h3[@class = 'lister-item-header']/a/text()").get(),
                    'year': film.xpath(".//span[@class = 'lister-item-year text-muted unbold']/text()").get(),
                    'duration': film.xpath(".//span[@class = 'runtime']/text()").get(),
                    'genre': film.xpath("normalize-space(.//span[@class = 'genre']/text())").get(),
                    'meta_score': film.xpath("normalize-space(.//span[@class = 'metascore  mixed']/text())").get(),
                    'description': film.xpath("normalize-space(.//p[@class = 'text-muted'])").get(),
                    'directors/actors': film.xpath(".//p[contains(text() , 'Director')]/a/text()").getall(),
                    'rate' : film.xpath(".//div[@class = 'inline-block ratings-imdb-rating']/strong/text()").get(),
                    'votes' : film.xpath(".//p[@class = 'sort-num_votes-visible']/span[2]/text()").get(),
                    'Gross' : film.xpath(".//span[contains(text(), 'Gross')]/following::span[1]/text()").get(),
                }

        next_page = response.xpath("(//a[@class = 'lister-page-next next-page'])[2]/@href").get()
        next_page_link = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url = next_page_link , callback=self.parse)
        else:
            sys.exit()