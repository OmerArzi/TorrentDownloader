from py1337x import py1337x
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
from Series import Series
import pickle


def get_series():
    name = input('Enter series name: ')
    season = int(input('Enter season: '))
    download_all = input("Download all (Yes/No): ")
    if download_all == 'Yes':
        download_all = True
    else:
        download_all = False
    res_series = Series(name, season, download_all)
    return res_series


def find_best(search_results):
    result = search_results['items'][0]
    for search_result in search_results['items']:
        if search_result['points'] > result['points']:
            result = search_result
    return result


def prioritize_link(search_results):
    for search_result in search_results['items']:
        search_result['points'] = 0
        if '1080p' in search_result['name']:
            search_result['points'] += 3
        elif '720p' in search_result['name']:
            search_result['points'] += 1
        if '⭐' in search_result['name']:
            search_result['points'] += 1
        if 'YIFY' in search_result['name']:
            search_result['points'] += 1.5
    return find_best(search_results)


def notification_hotkeys_combo(comp, driver):
    comp.send_keys(Keys.ENTER)
    pyautogui.hotkey('1', interval=0.6)
    pyautogui.hotkey('right', interval=0.6)
    pyautogui.hotkey('enter', interval=0.5)
    driver.close()


def pass_on_season(torrents_list, chosen_series):
    first_time = False
    search_result = torrents_list.search(str(chosen_series))
    while len(search_result['items']) != 0:
        prioritized_link = prioritize_link(search_result)
        driver = webdriver.Chrome(executable_path=r"C:\Users\Omer\Downloads\chromedriver.exe")
        driver.get(prioritized_link['link'])
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        comp = driver.find_element_by_xpath("/html/body/main/div/div/div/div[2]/div[1]/ul[1]/li[1]/a")
        if first_time is False:
            driver.implicitly_wait(0.5)
        first_time = False
        notification_hotkeys_combo(comp, driver)
        chosen_series.episode += 1
        search_result = torrents_list.search(str(chosen_series))


def init():
    torrents = py1337x()
    series = get_series()
    return torrents, series


def prog_start(torrents, series):
    if series.all is False:
        pass_on_season(torrents, series)
    else:
        search_result = torrents.search(str(series))
        prev_season = series.season
        series.season = 1
        while len(search_result['items']) != 0:
            pass_on_season(torrents, series)
            series.season += 1
            series.episode = 1
            search_result = torrents.search(str(series))
        exit(0)


torrents, series = init()
prog_start(torrents, series)
