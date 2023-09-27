import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bridgelegal.items import BridgelegalItem


def convert(case):
    case = case.lower()
    res = case.replace(' ', '-')
    return res


class BlSpider(scrapy.Spider):
    name = "bl"
    allowed_domains = ["www.lawsuit-information-center.com"]
    start_urls = ["http://www.lawsuit-information-center.com/"]
    base_url = "http://www.lawsuit-information-center.com/category/mass-torts/"
    def parse(self, response):
        case_list = response.xpath('//div[@id="custom_html-6"]//li/ul/li/a')
        # exclute state info
        case_list = case_list[0:12]
        for c in case_list:
            case = c.xpath('./text()').extract_first()
            href = c.xpath('./@href').extract_first()
            # request to visit the case articles link
            yield scrapy.Request(url=href, callback=self.parse_second, meta={'case': case, 'page': 1})

    def parse_second(self, response):
        # if self.page < 2:
        #     self.page = self.page + 1
        #     url = str(self.base_url) + str(self.page) + '-cp01.01.02.00.00.00.html'
        #     # scrapy.Requestju是scrapy 的get 请求
        #     yield scrapy.Request(url=url, callback=self.parse)
        article_list = response.xpath('//div[@class="inner-wrapper"]//h2//a')
        date_list = response.xpath('//div[@class="inner-wrapper"]//time')

        # case name
        case = response.meta['case']
        page = response.meta['page']
        for i in range(len(article_list)):
            a = article_list[i]
            # article name
            article = a.xpath('./text()').extract_first()
            # article url
            url = a.xpath('./@href').extract_first()
            # article date
            date = date_list[i].xpath('./text()').extract_first()
            item = BridgelegalItem(case=case, article=article, url=url, date=date)
            yield item

        if page < 10:
            page += 1
            url_convert = convert(case)
            url = self.base_url + url_convert + '/page/' + str(page)
            try:
                yield scrapy.Request(url=url, callback=self.parse_second, meta={'case': case, 'page': page})
            except Exception as e:
                self.logger.error(f"Error occurred: {str(e)}")
