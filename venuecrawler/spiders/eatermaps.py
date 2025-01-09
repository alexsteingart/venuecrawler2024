import scrapy

class EaterMaps(scrapy.Spider):
    name = 'eatermaps'
    start_urls = ['https://ny.eater.com/maps/archives']

    def parse(self, response):
        for anchor in response.css('div.c-entry-box--compact h2 a'):
            yield response.follow(anchor, callback=self.parse_map)

    def parse_map(self, response):
        for r in response.css('section.c-mapstack__card'):
            item = {}
            item['address'] = r.css('div.c-mapstack__address a::text').extract_first()
            if not item['address']: continue

            item['venue_name'] = r.css('h1::text').extract_first()
            item['description'] = ' '.join(r.css('div.c-entry-content').css('::text').getall())
            item['gmaps_url'] = r.css('div.c-mapstack__address a::attr(href)').get()
            item['website'] = r.css('a[data-analytics-link="link-icon"]::attr(href)').get()
            item['site'] = 'Eater Maps'
            item['site_url'] = response.url
            item['site_title'] = response.css('title::text').extract_first()
            item['territory'] = 'NYC'
            yield item
