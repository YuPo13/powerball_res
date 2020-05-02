"""This module describes the mechanism of scraping url creation
based on recent date and Monday-to-Monday 3-months period (backwards)"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

scraping_end_date = (datetime.today() - timedelta(days=datetime.today().weekday()))
scraping_start_date = scraping_end_date - relativedelta(months=3) - timedelta(days=1)

url_for_scraping = f"https://lottery.com/results/us/powerball/?start={scraping_start_date.strftime('%m/%d/%y')}" \
                       f"&end={scraping_end_date.strftime('%m/%d/%y')}"