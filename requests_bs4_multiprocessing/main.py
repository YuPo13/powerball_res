from bs4 import BeautifulSoup
import requests
import csv
from multiprocessing import Pool
from dates_for_urls import urls


def get_data(link):
    data = []
    result = requests.get(link)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        games = soup.select(".lottery-vertical-view-items.clearfix")
        for game in games:
            game_result = dict()
            game_result["name"] = game.select_one(".title-column").text.strip()
            game_result["draw_date"] = game.select_one(".date-column > div").text.strip()
            game_result["jackpot"] = game.select_one(".jackpot-column > span").text.strip("Jackpot")
            win_numbers = game.select(".results-column .lottery-item-winnumbers .lottery-ball-wrap > div > span")
            win_numbers_sequence = []
            for number in win_numbers:
                figure = number.text.strip()
                win_numbers_sequence.append(figure)
            game_result["win_numbers"] = ", ".join(win_numbers_sequence).strip(", ")
            data.append(game_result)
    return data


with open("3m_powerball_results_rbm.csv", "w", newline="") as infile:
    csv_names = ["name", "draw_date", "jackpot", "win_numbers"]
    writer = csv.DictWriter(infile, fieldnames=csv_names)
    writer.writeheader()
    pool = Pool(len(urls))
    final_data = pool.map(get_data, urls)
    pool.terminate()
    pool.join()
    for item in final_data:
        for share in item:
            writer.writerow(share)
