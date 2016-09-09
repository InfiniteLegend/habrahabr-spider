#Habrahabr spider
Spiders that crawls [Habrahabr](https://habrahabr.ru) site using Scrapy framework.
All results are sending to MongoDB or AWS ES server (if those pipelines where defined in **local_settings.py**)

Example:
```
ITEM_PIPELINES = {
   'habrahabr.pipelines.MongoPipeline': 0,
   'habrahabr.pipelines.ElasticsearchPipeline': 1,
}

ELASTICSEARCH_URL = ""
ELASTICSEARCH_INDEX = ""

MONGO_URI = ""
MONGO_DATABASE = ""
MONGO_COLLECTION = ""
```

To disable any of this pipelines, simply don't mention them in **ITEM_PIPELINES** (it's all in your hands, I warned :))

To install scrapy you need to install plenty of packages.

*For Linux [Solution](https://medium.com/@kaismh/extracting-data-from-websites-using-scrapy-e1e1e357651a#.ve51mjlan):
`sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev`

**Create _local\_settings.py_ file with YOUR Mongo and AWS ES credentials**
