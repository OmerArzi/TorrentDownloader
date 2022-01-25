from Py1337x import Py1337x
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pyautogui
from Series import Series
import WatchStatusDBM as db


# TODO: Validate updating (update database after confirming requested episode is being downloaded (could be via torrent name)).


def get_series():
    name = input('Enter series name: ')
    download_all = input("Download all (y/n): ").lower()
    if download_all == 'y':
        download_all = True
    else:
        download_all = False
    res_series = Series(name)
    return res_series


def find_best(search_results):
    result = search_results[0]
    for search_result in search_results:
        if search_result['points'] > result['points']:
            result = search_result
    return result


def prioritize_link(search_results):
    for search_result in search_results:
        search_result['points'] = 0
        if '1080p' in search_result['title']:
            search_result['points'] += 3
        elif '720p' in search_result['title']:
            search_result['points'] += 1
        if '⭐' in search_result['title']:
            search_result['points'] += 1
        if 'YIFY' in search_result['title']:
            search_result['points'] += 1.5
        if 'CAKES' in search_result['title']:
            search_result['points'] += 0.5
    return find_best(search_results)


def notification_hotkeys_combo(driver, first_time: bool):
    if first_time is False:
        driver.implicitly_wait(0.2)
    pyautogui.hotkey('1', interval=0.1)
    pyautogui.hotkey('right', interval=0.2)
    pyautogui.hotkey('enter', interval=0.2)
    driver.close()
    return False


def download_single_season(torrents_list, chosen_series):
    first_time = True
    search_result = torrents_list.search(str(chosen_series))
    while len(search_result) != 0:
        prioritized_link = prioritize_link(search_result)
        # s = Service(r"C:\Users\Omer\Downloads\chromedriver.exe")
        driver = webdriver.Chrome(r"C:\Users\Omer\Downloads\chromedriver.exe")
        driver.get(prioritized_link['MagnetLink'])
        first_time = notification_hotkeys_combo(driver, first_time)
        # TODO: Add file path to function call (to 'chosen_series.create_episode_path':)
        chosen_series.create_episode_path(prioritized_link['title'])
        chosen_series.episode += 1
        chosen_series.update_episode()
        search_result = torrents_list.search(str(chosen_series))


def init_parameters():
    torrents = Py1337x()
    series = get_series()
    return torrents, series


def program_start(torrents: Py1337x, series: Series):
    if not series.all:
        download_single_season(torrents, series)
    else:
        search_result = torrents.search(str(series))
        series.season = 1
        while len(search_result) != 0:
            download_single_season(torrents, series)
            series.season += 1
            series.episode = 1
            search_result = torrents.search(str(series))
        exit(0)


def main():
    torrents, series = init_parameters()
    # TODO: Create folder according to series name
    program_start(torrents, series)


if __name__ == '__main__':
    main()
