"""This module describes the mechanism of scraping urls creation
based on recent date and Monday-to-Monday 3-months weekly periods (backwards)"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

scraping_end_date = (datetime.today() - timedelta(days=datetime.today().weekday()))
scraping_start_date = scraping_end_date - relativedelta(months=3) - timedelta(days=1)
scraping_start_week_date = scraping_end_date - timedelta(days=7)

urls = list()

while scraping_start_date <= scraping_start_week_date:
    url_for_scraping = f"https://lottery.com/results/us/powerball/?start=" \
                       f"{scraping_start_week_date.strftime('%m/%d/%y')}&end={scraping_end_date.strftime('%m/%d/%y')}"
    urls.append(url_for_scraping)
    scraping_end_date = scraping_start_week_date
    scraping_start_week_date = scraping_start_week_date - timedelta(days=7)