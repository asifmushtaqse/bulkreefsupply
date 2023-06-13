from scrapy.crawler import CrawlerProcess

from bulkreefsupply_spider import BulkReefSupplyBRSSpider


def run_spider_via_python_script():
    process = CrawlerProcess()
    process.crawl(BulkReefSupplyBRSSpider)
    process.start()


if __name__ == "__main__":
    run_spider_via_python_script()
    pass
