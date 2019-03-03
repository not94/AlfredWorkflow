# -*- coding:utf-8 -*-
import json
import sys
import os
from urllib.parse import quote

from lib import feedparser


class RSSSpider(object):

    # rss url
    BASE_URL = "https://www.dmhy.org/topics/rss/rss.xml"
    SEARCH_URL = "https://www.dmhy.org/topics/rss/rss.xml?keyword={}"
    TEAM_URL = "https://share.dmhy.org/topics/rss/team_id/{}/rss.xml"
    CATEGORY_URL = "https://share.dmhy.org/topics/rss/sort_id/{}/rss.xml"

    # command enum
    COMMAND_KEYWORD = "keyword"  # 关键字订阅
    COMMAND_TEAM = "team"  # 联盟订阅
    COMMAND_CATEGORY = "category"  # 分类订阅

    # command url map
    COMMAND_URL_MAP = {
        COMMAND_KEYWORD: SEARCH_URL,
        COMMAND_TEAM: TEAM_URL,
        COMMAND_CATEGORY: CATEGORY_URL
    }

    def __init__(self, command, arg=None):
        self.command = command
        self.arg = arg
        self._raw = None

    def make_complete_url(self):
        return self.COMMAND_URL_MAP.\
            get(self.command, self.BASE_URL).format(quote(self.arg))

    def init_raw_data(self):
        if self._raw is None:
            url = self.make_complete_url()
            self._raw = feedparser.parse(url)

    @property
    def items(self):
        self.init_raw_data()
        return self._raw.entries

    @staticmethod
    def make_title(title):
        """去掉第一个[]"""
        begin_marks = ["[", "【"]
        end_marks = ["]", "】"]
        begin_index = end_index = None
        for i, s in enumerate(title):
            if s in begin_marks:
                begin_index = i
            if s in end_marks:
                end_index = i
                break
        if begin_index is not None and end_index is not None:
            return title[:begin_index] + title[end_index + 1:]
        return title

    @staticmethod
    def get_item_magnet(item):
        for link in item.links:
            if link.type == "application/x-bittorrent":
                return link.href
        return ''

    def serialize(self):
        return json.dumps(
            {
                "items": [
                    {
                        "title": self.make_title(item.title),
                        "subtitle": item.title,
                        "arg": item.link,
                        "variables": {
                            "link": item.link,
                            "magnet": self.get_item_magnet(item)
                        }
                    }
                    for item in self.items
                ]
            },
            ensure_ascii=False
        )


if __name__ == '__main__':
    command = os.environ.get("command", RSSSpider.COMMAND_KEYWORD)
    keyword = u"".join(sys.argv[1:])
    print(RSSSpider(command, keyword).serialize())
