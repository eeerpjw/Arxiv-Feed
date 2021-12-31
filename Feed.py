# -*- coding: utf-8 -*-
# @Time : 2021/12/25 10:26 AM
# @Author : "liam"
# @Email : cs_pjw@163.com
# @File : Feed.py
# @Software: VS code

import feedparser
import yaml
import os
import re

def make_bold(keywords, text):
    for kw in keywords:
        if kw in text:
            text = text.replace(kw, '**'+kw+'**')
    return text

class ArxivFeed(object):
    def __init__(self, feed: object, category: str, keywords: list, authors: list) -> None:
        self.tag = category
        self.keywords = keywords
        self.authors = authors
        #self.feed = feedparser.parse(self.rss_link)
        self.feed = feed
        # 今日所有的title
        self.titles = []
        # 查找感兴趣的论文
        self.selected = []
        nameRegex = re.compile('[A-Za-z]{2,25} [A-Za-z]{2,25}')
        for entry in self.feed.entries:
            # print(entry['id'])
            entry["summary"] = entry["summary"].replace("\n", " ")
            in_summary = any([kw in entry["summary"] for kw in self.keywords]
                             ) if self.keywords is not None else False
            in_title = any([kw in entry["title"] for kw in self.keywords]
                           ) if self.keywords is not None else False
            in_author = any([au in entry["author"] for au in self.authors]
                            ) if self.authors is not None else False
            if in_author or in_summary or in_title:
                author_lst = nameRegex.findall(entry["author"])
                sel_entry = {"title": entry["title"],
                             "link": entry["link"],
                             "author": ", ".join(author_lst),
                             "abstract": entry["summary"].replace("<p>", " ").replace("</p>", " ")
                             }
                # 关键词加粗
                if in_author:
                    sel_entry['title'] = make_bold(
                        self.keywords, sel_entry['title'])
                elif in_title:
                    sel_entry['author'] = make_bold(
                        self.authors, sel_entry['author'])
                elif in_summary:
                    sel_entry['abstract'] = make_bold(
                        self.keywords, sel_entry['abstract'])
                self.selected.append(sel_entry)
            self.titles.append(entry["title"])

    def convert2text_selected(self):
        s = '---\n'
        for entry in self.selected:
            s += '{} {}\n'.format("###", entry["title"])
            s += '{} : {}\n'.format("- Authors", entry["author"])
            s += '{} : [{}]({})\n'.format("- Link",
                                          entry["link"], entry["link"])
            s += '{} : {}\n'.format("> ABSTRACT ", entry["abstract"])
        return s

    def convert2text_paperlist(self):
        # print("## Paper list")
        s = '---\n'
        s += "**{}** new papers in {}:-) \n".format(len(self.titles), self.tag)
        for i, p in enumerate(self.titles):
            s += "{}. {}\n".format(i+1, p)
        return s

    def print_selected(self):
        print("## Your Interest")
        print(self.convert2text_selected())

    def print_paperlist(self):
        print("## Paper list")
        print(self.convert2text_paperlist())

    def summary():
        pass

    def send_me_via_email():
        pass
