import scrapy
from scrapy.http import HtmlResponse

from bilibili_test.items import ArticleItem, ArticleImageItem


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']

    # url方式一：初始请求数组
    # start_urls = ['https://www.xxx.com/xxx']

    # url方式二：start_requests()方法发起请求
    def start_requests(self):
        print('Spider--start_requests()')
        # 爬取多页数据
        for page in range(1, 2):
            print('Spider--start_requests()--for')
            # 手动发起请求，每次请求一个url，使用模板字符串拼接页数
            yield scrapy.Request(f'https://search.bilibili.com/article?vt=67519417&keyword=%E5%A4%8F%E6%97%A5%E9%87%8D%E7%8E%B0&from_source=webtop_search&spm_id_from=333.1007&search_source=2&page={page}')

    def parse(self, response: HtmlResponse):
        print('Spider--parse()')
        list_items = response.css('body > #server-search-app .body-contain .article-item')
        for list_item in list_items:
            article_item = ArticleItem()
            # css()和xpath()方法返回的是selector列表
            # extract()方法将selector列表解析成字符串列表
            # extract_first()方法将selector列表中第一个数据解析成字符串并返回该字符串
            article_item['link'] = list_item.css('a img::attr(src)').extract_first()
            article_item['title'] = list_item.css('.content >.headline>a::attr(title)').extract_first()
            article_url = "https:" + list_item.css('.content >.headline > a::attr(href)').extract_first()
            print('Spider--parse()--for')
            # 将article_item信息发送到管道
            yield article_item

            # 调用parse_article()方法解析详细信息
            # 请求传惨：通过meta参数传递一个map，目标方法可以接收
            yield scrapy.Request(article_url, self.parse_article_image, meta={'article_item': article_item})

    # 自定义解析文章详情页的方法，用于提取图片
    def parse_article_image(self, response):
        # 获取传递的参数
        article_item = response.meta['article_item']
        print(f"获取文章《{article_item['title']}》的图片")
        figure_list = response.css('#article-content > #read-article-holder figure')
        for figure_item in figure_list:
            image_url = "https:" + figure_item.css('::attr(data-src)').extract_first()
            image_item = ArticleImageItem()
            image_item['src'] = image_url
            yield image_item
