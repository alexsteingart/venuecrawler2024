import scrapy

class TheInfatuation(scrapy.Spider):
    name = 'theinfatuation'
    start_urls = ['https://www.theinfatuation.com/new-york/reviews?page=1']
    MAX_PAGES=50
    PAGES = 0

    def parse(self, response):
        for anchor in response.css('a.chakra-linkbox__overlay'):
            yield response.follow(anchor, callback=self.parse_review)

        if self.PAGES < self.MAX_PAGES:
            for anchor in response.css('a.styles_loadMoreButton___IN38.css-1lkjr1d'):
                self.PAGES += 1
                yield response.follow(anchor, callback=self.parse)

    def parse_review(self, response):
        item = {}
        item['gmaps_url'] = response.css('a[data-testid="venue-googleMapUrl"]::attr(href)').extract_first()
        address_start = item['gmaps_url'].index('query=')
        if address_start > -1:
            item['venue_name'] = response.css('h1::text').extract_first()
            address_start +=  6 + len(item['venue_name']) + 1
            item['address'] = item['gmaps_url'][address_start:]

            item['description'] = ' '.join(response.css('p.css-orc1vi').css('::text').getall())
            item['website'] = response.css('a[data-testid="venue-url"]::attr(href)').get()
            item['site'] = 'The Infatuation'
            item['site_url'] = response.url
            item['site_title'] = response.css('title::text').extract_first()
            item['site_published_date'] = response.css('time[datetime]::text').get()
            item['territory'] = 'NYC'
            yield item
