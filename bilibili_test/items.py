# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 封装文章数据
class ArticleItem(scrapy.Item):
    # 属性的定义方式如下:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()

# 封装文章图片地址
class ArticleImageItem(scrapy.Item):
    src = scrapy.Field()
