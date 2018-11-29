# -*- coding: utf-8 -*-
import scrapy

from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class VirtueSpider(CrawlSpider):
    name = 'virtue'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']

    #rules = (Rule(LinkExtractor(allow=()),callback="parse", follow=True),)
    rules = [
        Rule(LinkExtractor(allow=()), follow=True, callback='parse_item')
    ]
    cnt = 0
    words = ["Virtue", "signalling", "is", "society", "version", "of", "Proof", "Stake"]
    result = {}
    result_printed = False

    def parse_item(self, response):
        print('Processing... ' + response.url)
        self.find(str(response.body), response.url)
        if len(self.result) == len(self.words):
            if not self.result_printed:
                for k, v in self.result.items():
                    print('Found {} in url: {}'.format(k, v))
                self.result_printed = True
            raise CloseSpider('All words found')

    def find(self, text, url):
        for word in self.words:
            if word in self.result:
                continue
            if word.lower() in text.lower():
                self.result[word] = url
                print('Found word: ', word)
