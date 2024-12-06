import scrapy

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [start_url.split('//')[1].split('/')[0]]

    def parse(self, response):
        text = ' '.join(response.css('::text').getall()).strip()
        yield {
            'url': response.url,
            'text': text
        }

        for href in response.css('a::attr(href)').getall():
            yield response.follow(href, self.parse)
