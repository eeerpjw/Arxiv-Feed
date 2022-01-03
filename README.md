# Arxiv-Feed
## Requirement
python==3.8
pyyaml==6.0
feedparser==6.0.8
## How-to
### Set Your Interest via Editing ./configs/list.yaml
1. You can add any keywords and authors as you like.
2. Add RSS items, eg. Eg. ```cs.CV```, below. Follow [RSS news feeds for arXiv updates](https://arxiv.org/help/rss) for more details about RSS link rules in ArXiv.
3. Note that there are common keywords/authors cross-rss-items and specified keywords/authors for each items.

### Run
```bash
cd ./Arxiv-Feed/;python main.py;
```

## TO-DO
- [ ] 去除重复论文/计数 (能用就行，不打算改了)
- [ ] IEEE Transactions