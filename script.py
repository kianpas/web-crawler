from scrapy import item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item, Field

class MyItems(Item):
    referer = Field()
    response = Field()
    status = Field()

class MySpider(CrawlSpider):
    name = "test-crawler"
    target_domains = ["dev.to"]
    start_urls = ["https://dev.to/"]
    handle_httpstatus_list = [404, 410, 301, 500]

    custom_setting = {
         'CONCURRENT_REQUESTS': 2,
         'DOWNLOAD_DELAY' : 0.5
    }

    rules = [
        Rule(
            LinkExtractor( allow_domains=target_domains, deny=('patterToBeExcluded'), unique=('Yes')),
            callback='parse_my_url',
            follow=True
        ),
        Rule(
            LinkExtractor ( allow=(''), deny=('patterToBeExcluded'), unique=('Yes')),
            callback='parse_my_url',
            follow=False
        )
    ]

def parse_my_url(self, response):
    report_if = [404, 400, 500, 200]
    if response.status in report_if:
        item = MyItems()                               
        item['referer'] = response.request.headers.get('Referer', None)
        item['status'] = response.status
        item['response'] = response.url
        yield item
    yield None
