# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.pipelines.images import ImagesPipeline

from bilibili_test.items import ArticleItem, ArticleImageItem


# 将文章信息存储到mysql数据库
class MysqlPipeline:
    # 数据库连接
    conn = None
    # 数据库游标多谢
    cursor = None

    # 该方法会在爬虫开始时被调用并且只会被调用一次
    def open_spider(self, spider):
        print('mysql管道--open_spider()')
        self.conn = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            db='scrapy_test',
            charset='utf8',
        )

    # 接收爬虫文件传递过来的item对象
    def process_item(self, item: ArticleItem, spider):
        print('mysql管道--process_item()')
        if not isinstance(item, ArticleItem):
            # 如果不是需要的类型，直接发送到下一个管道
            return item
        # 写入文件
        self.cursor = self.conn.cursor()
        # 插入到mysql
        try:
            self.cursor.execute('insert into article(title,link) values("%s","%s")' % (item["title"], item["link"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    # 爬虫结束后会调用一次
    def close_spider(self, spider):
        print('mysql管道--close_spider()')
        self.conn.close()


# 声明父类是ImagesPipeline
# ImagesPipeline是scrapy提供的专门用于图片存储的管道类
class ArticleImagePipeline(ImagesPipeline):
    # 根据图片地址进行图片数据的请求
    def get_media_requests(self, item, info):
        print('图片下载管道--get_media_requests()')
        if not isinstance(item, ArticleImageItem):
            # 如果不是需要的类型，直接发送到下一个管道
            return item
        # 获取图片
        yield scrapy.Request(item['src'])

    # 指定文件存储位置
    def file_path(self, request, response=None, info=None, *, item=None):
        print('图片下载管道--file_path()')
        imageName = request.url.split('/')[-1]
        return imageName

    # 用于该管道执行结束向下一个将要执行的管道传递数据
    # 如果不需要传递数据，则这个方法可以不重写
    def item_completed(self, results, item, info):
        print('图片下载管道--item_completed()')
        # 把当前的item传递给下一个管道类
        return item
