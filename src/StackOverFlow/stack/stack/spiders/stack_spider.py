'''
Creating a spider to crawl stackoverflow

docs: https://doc.scrapy.org/en/1.0/topics/spiders.html#spider
'''


from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com']
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        # XPath states: Grab all <h3> elements
        # children of a <div> that has a class of summary
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
