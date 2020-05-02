from lxml import etree
import requests
import csv
from dates_for_urls import urls
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_data(link):
    data = []
    result = requests.get(link)
    if result.status_code == 200:
        passage_to_parse = etree.HTML(str(result.content))
        games = passage_to_parse.xpath("//*[@class='lottery-vertical-view-items clearfix']")
        for game in games:
            names = game.xpath('//*[@class="title-column"]/text()')
            dates = game.xpath('//*[@class="date-column"]/div/text()')
            jackpots = game.xpath('//*[@class="jackpot-column"]/span/text()')
            all_win_numbers = game.xpath('//*[@class="results-column"]/div[@class="lottery-item-winnumbers"]'
                                         '/div[@class="lottery-ball-wrap"]/div/span/text()')
            win_numbers = [all_win_numbers[x:x+6] for x in range(0, len(all_win_numbers), 6)]
            final_dataset = zip(names, dates, jackpots, win_numbers)
            for data_piece in final_dataset:
                game_result = dict()
                game_result["name"] = data_piece[0]
                game_result["draw_date"] = data_piece[1]
                game_result["jackpot"] = data_piece[2]
                game_result["win_numbers"] = ", ".join(data_piece[3]).strip(", ")
                writer.writerow(game_result)
            break


if __name__ == '__main__':
    with open("3m_powerball_results_rlcft.csv", "w", newline="") as infile:
        csv_names = ["name", "draw_date", "jackpot", "win_numbers"]
        writer = csv.DictWriter(infile, fieldnames=csv_names)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            futures = [executor.submit(get_data, url) for url in urls]

