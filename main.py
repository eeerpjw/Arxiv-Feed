# -*- coding: utf-8 -*-
# @Time : 2021/12/25 10:26 AM
# @Author : "liam"
# @Email : cs_pjw@163.com
# @File : main.py
# @Software: VS code

import yaml
import os
import datetime
from Feed import ArxivFeed

def main():
    with open("./configs/list.yaml","r") as f:
        opt = yaml.load(f, Loader=yaml.FullLoader)
    interest = ''
    all_paper = ''
    # 按照日期保存
    save_path = "./history/arxiv_{}.md".format(datetime.date.today())
    os.makedirs(os.path.dirname(save_path),exist_ok=True)
    num_interest = 0
    for keys in opt:
        if keys=='common':
            continue
        interest+='## {}\n'.format(keys)
        all_paper+='## {}\n'.format(keys)
        keywords=opt[keys]["keywords"]+opt["common"]["keywords"] \
            if opt[keys]["keywords"] is not None else opt["common"]["keywords"]
        authors=opt[keys]["authors"]+opt["common"]["authors"] \
            if opt[keys]["keywords"] is not None else opt["common"]["authors"]
        # print("# {}".format(keys))
        fd = ArxivFeed(link=opt[keys]["link"],
                        keywords=keywords,
                        authors=authors
                        )
        interest += fd.convert2text_selected()
        all_paper+=fd.convert2text_paperlist()
        num_interest += len(fd.selected)
    interest = '# Your interest papers\n---\n'+interest
    all_paper = '# Paper List\n---\n'+all_paper
    with open(save_path,'w') as f:
        f.write(interest+all_paper)
    # 用vscode预览
    print(num_interest)
    os.system("code {}".format(save_path))
    
if __name__=="__main__":
    main()