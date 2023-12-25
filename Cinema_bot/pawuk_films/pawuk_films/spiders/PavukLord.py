import scrapy
from logger import logger
from pawuk_films.items import PawukFilmsItemLord

class PavuklordSpider(scrapy.Spider):
    name = "PavukLord"
    allowed_domains = ["hd.hdrfilm.info"]
    start_urls = []

    #add all the pages on which the spider will run
    for i in range (1, 80):
        start_urls.append(f"https://hd.hdrfilm.info/multfilms/page/{i}")
        
    for i in range(1, 722):
        start_urls.append(f"https://hd.hdrfilm.info/filmy-v1/page/{i}")
    
    for i in range (1, 188):
        start_urls.append(f"https://hd.hdrfilm.info/serialys/page/{i}")
    

    def parse(self, response):
        for link in response.css('div.th-item a::attr(href)').getall():
            yield response.follow(link, callback=self.parse_one)

    def parse_one(self, response):
        film = PawukFilmsItemLord()
        film['link'] = response
        film['name'] = response.css('div.fleft-desc h1::text').get()

        #as ratings KP and IMDB not everywhere, add them carefully
        if response.css('div.frate span').getall()[0] == '<span></span>':
            if response.css('div.frate span').getall()[1] == '<span></span>':
                rating_kp = None
                rating_imdb = None
            else:
                rating_kp = None
                rating_imdb = response.css('div.frate span::text').get()
        if response.css('div.frate span').getall()[1] == '<span></span>':
            if response.css('div.frate span').getall()[0] == '<span></span>':
                rating_kp = None
                rating_imdb = None
            else:
                rating_imdb = None
                rating_kp = response.css('div.frate span::text').get()
        if response.css('div.frate span').getall()[0] != '<span></span>' and response.css('div.frate span').getall()[1] != '<span></span>':
            rating_kp = response.css('div.frate span::text').getall()[0]
            rating_imdb = response.css('div.frate span::text').getall()[1]

        film['rating_kp'] = rating_kp
        film['rating_imdb'] = rating_imdb

        #add the description
        description = response.css('div.fleft-desc div.fdesc::text').get().split()
        string = ''
        for i in description:
            string = string + i + ' '
        film['description'] = string[:-1]

        #add countries and genres
        film['country'] = response.css('div.flists li::text').getall()[2].split(', ')
        film['genres'] = response.css('ul.flist span::text').getall()[-1].split(', ')

        #flag: film/series/multfilm
        if response.css('div.speedbar a::attr(href)').getall()[1] == 'https://hd.hdrfilm.info/serialys/':
            film['film_or_series'] = 'series'
        elif response.css('div.speedbar a::attr(href)').getall()[1] == 'https://hd.hdrfilm.info/multfilms/':
            film['film_or_series'] = 'multfilm'
        else:
            film['film_or_series'] = 'film'

        #poster
        film['poster'] = 'https://hd.hdrfilm.info/' + response.css('div.fposter img::attr(src)').get()
        logger.info("This film has been successfully parsed")
        yield film

        