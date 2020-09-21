# -*- coding: utf-8 -*-
import scrapy


class EbayCrawlerSpider(scrapy.Spider):
    name = 'ebay_crawler'
    allowed_domains = ['www.ebay.com']

    def start_requests(self):
        query = input("Enter what you're seaching for\n"+
                      "Replace spaces by '+' signs\n"+
                      ">> ")
        yield scrapy.Request(url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={query}&_sacat=0' , callback=self.parse,
                             headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.104'})

    def parse(self, response):
        data = response.xpath("//li[starts-with(@class, 's-item    ')]")
        for product in data:
            product_name = product.xpath('.//a[@class = "s-item__link"]/h3/text()').get()
            link = product.xpath('.//a[@class = "s-item__link"]/@href').get()
            price = product.xpath('.//span[@class = "s-item__price"]/text()').get()

            yield {
                'product' : product_name,
                'link' : link,
                'price' : price,
            }

        next_page = response.xpath('//a[@class = "pagination__next"]/@href').get()
        print(next_page)
        if next_page:
            yield scrapy.Request(url = next_page , callback=self.parse ,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.104'})