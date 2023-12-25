import scrapy
from logger import logger
from pawuk_films.items import PawukFilmsItemIvi
from pawuk_films.spiders.ivi_pages import genres, pages, series, series_pages, multfilms, multi_pages


class PavukiviSpider(scrapy.Spider):
    name = "PavukIvi"
    allowed_domains = ["www.ivi.ru"]
    start_urls = []
    
    #add all the pages on which the spider will run
    for g in genres:
        for i in range(pages[g]):
            start_urls.append('https://www.ivi.ru/movies/' + g + f'/page{i}')

    for s in series:
        for i in range(series_pages[s]):
            start_urls.append('https://www.ivi.ru/series/' + s + f'/page{i}')

    for m in multfilms:
        for i in range(multi_pages[m]):
            start_urls.append('https://www.ivi.ru/animation/' + m + f'/page{i}')

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            if '/watch/' in link:
                yield response.follow('https://www.ivi.ru' + link, callback=self.parse_one)

    def parse_one(self, response):
        film = PawukFilmsItemIvi()
        film['link'] = response
        film['name'] = response.css('div.watchTitle h1::text').get().split('(')[0][:-1]

        film['rating_ivi'] = response.css('div.nbl-ratingPlate__value::text').get()

        #add the description
        film['description'] = response.css('div.clause p::text').get()

        #add countries and genres
        listik = response.css('div.watchParams a::text').getall()
        film['country'] = listik[1]
        film['genres'] = listik[2::]

        #flag: film/series/multfilm
        if response.css('li.breadCrumbs__item a::attr(href)').get() == 'https://www.ivi.ru/series':
            film['film_or_series'] = 'series'
        elif response.css('li.breadCrumbs__item a::attr(href)').get() == 'https://www.ivi.ru/animation':
            film['film_or_series'] = 'multfilm'
        else:
            film['film_or_series'] = 'film'
        
        film['poster'] = response.css('div.playerBlock__video img::attr(src)').get()
        logger.info("This film has been successfully parsed")
        yield film

