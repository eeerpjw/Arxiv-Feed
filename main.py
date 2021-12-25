# -*- coding: utf-8 -*-
# @Time : 2021/12/25 10:26 AM
# @Author : "liam"
# @Email : cs_pjw@163.com
# @File : main.py
# @Software: VS code

import os
import yaml
import time
import datetime
import feedparser
from glob import glob
from Feed import ArxivFeed


def main():
    with open("./configs/list.yaml", "r") as f:
        opt = yaml.load(f, Loader=yaml.FullLoader)
    with open("./history/flag.yaml", "r") as f:
        flag = yaml.load(f, Loader=yaml.FullLoader)
    interest = ''
    all_paper = ''
    num_interest = 0
    for keys in opt:
        if keys == 'common':
            continue
        interest += '## {}\n'.format(keys)
        all_paper += '## {}\n'.format(keys)
        keywords = opt[keys]["keywords"]+opt["common"]["keywords"] \
            if opt[keys]["keywords"] is not None else opt["common"]["keywords"]
        authors = opt[keys]["authors"]+opt["common"]["authors"] \
            if opt[keys]["keywords"] is not None else opt["common"]["authors"]
        # print("# {}".format(keys))
        feed = feedparser.parse(opt[keys]["link"])
        last_update = time.strftime('%Y-%m-%d',feed.updated_parsed)
        if feed.date == flag[keys]:
            print("无（上次更新{}）".format(last_update))
            return 0
            #continue # 最近用过了
        else:
            flag[keys]=feed.date
        fd = ArxivFeed(feed=feed,
                       category = keys,
                       keywords=keywords,
                       authors=authors
                       )
        interest += fd.convert2text_selected()
        all_paper += fd.convert2text_paperlist()
        num_interest += len(fd.selected)
    interest = '# Your interest papers\n---\n'+interest
    all_paper = '# Paper List\n---\n'+all_paper
    save_path = "./history/arxiv_{}.md".format(last_update)
    # 按照日期保存
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w') as f:
        f.write(interest+all_paper)
    with open("./history/flag.yaml", "w") as f:
        yaml.dump(flag,f)
    # 用vscode预览
    print(num_interest)
    os.system("code {}".format(save_path))


if __name__ == "__main__":
    main()
