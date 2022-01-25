# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class singaporeexpatsPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            "localhost",
            27017
        )
        db = connection["expats"]
        self.collection = db

    def process_item(self, item, spider):
        valid = True

        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            if "topic" in item and "number_of_replies" in item and "number_of_views" in item:
                self.collection["topics"].insert_one(dict(item))
            else:
                self.collection["posts"].insert_one(dict(item))
        return item
