import scrapy


class SingaporeExpats(scrapy.Spider):
    name = 'singaporeexpats'

    start_urls = [
        'https://forum.singaporeexpats.com/viewforum.php?f=93',
    ]

    def parse(self, response):
        for topic_list in response.xpath('//ul[has-class("topiclist topics")]'):
            for topic in topic_list.xpath('li/dl'):
                yield {
                    'topic': topic.xpath('dt/div/a/text()').get(),
                    'number_of_replies': topic.xpath('dd[@class("posts")]/text()').get(),
                    'number_of_views': topic.xpath('dd[@class("views")]/text()').get(),
                }
                yield response.follow(topic.xpath('div/a/@href').get(), \
                    self.parse)

        for post in response.xpath('//div[has-class("post has-profile bg2")]/div/div[has-class("inner")]'):
            yield {
                'topic': post.xpath('div[@class("postbody")]/div/h3/a/text()').get(),
                'author': post.xpath('dl[@("postprofile")]/dt/a/text()').get(),
                'content': post.xpath('div[@("postbody")]/div/div[has-class("content")]/text()').get(),
            }

        next_page = response.xpath('//li[has-class("arrow next")]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
