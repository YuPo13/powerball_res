"""This module describes the mechanism of scraping url creation
based on recent date and Monday-to-Monday 3-months period (backwards)"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

scraping_end_date = (datetime.today() - timedelta(days=datetime.today().weekday())).strftime("%m/%d/%y")
scraping_start_date = (datetime.today() - timedelta(days=datetime.today().weekday()) -
                       relativedelta(months=3) - timedelta(days=1)).strftime("%m/%d/%y")

url_for_scraping = f"https://lottery.com/results/us/powerball/?start={scraping_start_date}&end={scraping_end_date}"
