How to run spider script after make setup & configuration
*******  How to Setup Documentation *******

** I am placing website url that will help you while installing virtual environment:
https://www.geeksforgeeks.org/python-virtual-environment/
**

The tool is made in python 3
extract it to your system.

*** Step-1 ***
-> You need to install an IDE for managing project. Please download and install
Editor PyCharm Community Edition.

-> you need to install some modules, just open terminal window in pycharm and write command:
pip install Scrapy==2.6.3
pip install scrapy-crawlera==1.7.2
pip install python-dotenv==0.21.1
pip install scrapy-rotating-proxies==0.6.2

OR

you can install all requirements using requirements.txt. Use this command:
pip install -r requirements.txt

if any issue you will face get help from:
https://www.youtube.com/watch?v=5JwPKGZUiSs

download libraries from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

sudo apt install --reinstall python3 python python3-minimal --fix-broken

Note: Now Set your project interpreter in which you have scrapy installed.

*** Step-2 ***
Before running make What to make sure is:
you are in the folder /bulkreefsupply/bulkreefsupply/spiders

Run script command:
python3 -m scrapy crawl bulkreefsupply_spider

OR

1.1) Run script at background:
nohup python3 -m scrapy crawl bulkreefsupply_spider &

Note: "bulkreefsupply_spider" is the name of spider, that scrape data.


2) Run Script command for scrape daily products:
Run script command:
python3 -m scrapy crawl brs_daily_products_spider

2.1) Run script at background:
nohup python3 -m s crawl brs_daily_products_spider &

Note: "brs_daily_products_spider" is the name of spider, that scrape data.



*** Step-3 ***
Now where will you get the output?
when you run script after completed Script execution,
then in the output folder you see "bulkreefsupply_products_{today_date}.json" file.

*** Step-4 ***
for any query please send me message.

Kind regards,
alifarslan


Schedule Cron Job to run by every Monday:
30 15 * * 1 python /home/deploy/crawlers/bulkreefsupply/bulkreefsupply/spiders/run_script.py # run_spider

* * * * * python /home/deploy/crawlers/bulkreefsupply/bulkreefsupply/spiders/test_cron_script.py # test_cron_2


Download File Path: https://archive.topshelfaquatics.com/output/bulkreefsupply_products_3.csv
Download File Path: https://archive.topshelfaquatics.com/output/test_time_file.txt

35 13 * * * python /home/deploy/crawlers/bulkreefsupply/bulkreefsupply/spiders/run_script.py # run_spider_2

nohup python /home/deploy/crawlers/bulkreefsupply/bulkreefsupply/spiders/run_script.py &

# Copy products file from scraper output folder to public html output folder
cp /home/deploy/crawlers/bulkreefsupply/bulkreefsupply/output/bulkreefsupply_products_3.csv /home/deploy/public_html/output/

Logs File: https://archive.topshelfaquatics.com/output/bulkreefsupply_spider_logs.log
Download File: https://archive.topshelfaquatics.com/output/bulkreefsupply_products_3.csv
