# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

proxy_ip_list = [
    '47.92.113.71:80',
    '117.157.197.18:3128',
    '111.23.16.250:3128',
]

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


# 爬虫中间件
class BilibiliTestSpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        print('爬虫中间件--from_crawler()')
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 下载器获得响应后，发送给spider之前会调用该方法
    def process_spider_input(self, response, spider):
        print('爬虫中间件--process_spider_input()')
        # 返回None或一个异常
        # 如果是None,就继续调用其他的spider middleware。
        # 如果是一个异常，调用request里的errback()方法，再抛出异常是交给process_spider_exception(response, exception, spider)处理
        return None

    # spider生成的结果发送给调度器之前被调用
    def process_spider_output(self, response, result, spider):
        print('爬虫中间件--process_spider_output()')
        # 必须返回一个包括request或item对象的可迭代对象
        for i in result:
            yield i

    #
    def process_spider_exception(self, response, exception, spider):
        # 当spider或其他中间件的process_spider_input()报错时被调用
        print('爬虫中间件--process_spider_exception()')
        # 应该返回 None 或一个可迭代的 Request 或 item 对象
        pass

    # 爬虫启动请求
    def process_start_requests(self, start_requests, spider):
        print('爬虫中间件--process_start_requests()')
        # 只能返回request对象
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        print('爬虫中间件--spider_opened()')
        spider.logger.info('Spider opened: %s' % spider.name)


# 下载中间件
class BilibiliTestDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # Scrapy 使用此方法来创建爬虫
        print('下载中间件--from_crawler()')
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 拦截请求，当每个request通过下载中间件时，该方法被调用
    def process_request(self, request, spider):
        print('下载中间件--process_request()')
        # 随机选择user-agent
        ua = random.choice(user_agent_list)
        # 设置请求的ua
        request.headers['User-Agent'] = ua
        return None

    # 拦截响应，
    def process_response(self, request, response, spider):
        print('下载中间件--process_response()')
        return response

    # 拦截发生异常的请求
    def process_exception(self, request, exception, spider):
        print('下载中间件--process_exception()')
        # 请求失败就设置代理ip
        if request.url.split(':') == 'https':
            # 设置代理ip
            request.meta['proxy'] = 'https//' + random.choice(proxy_ip_list)
        else:
            request.meta['proxy'] = 'http//' + random.choice(proxy_ip_list)
        # 返回request会重新进行请求发送
        return request

    def spider_opened(self, spider):
        print('下载中间件--spider_opened()')
        spider.logger.info('Spider opened: %s' % spider.name)
