from Py1337x import Py1337x
import os
from Series import Series
import sys
import subprocess
import WatchStatusDBM as db
from FileOrganizer import organize_single_series


# TODO New feature idea: search new episodes for all project in db.
# TODO Validate updating (update database after confirming requested episode is being downloaded (could be via torrent name)).

def get_series():
    name = input('Enter series name: ')
    download_all = input("Download all (y/n): ").lower()
    if download_all == 'y':
        download_all = True
    else:
        download_all = False
    res_series = Series(name, download_all)
    return res_series


# def find_best(search_results):
#     result = search_results[0]
#     for search_result in search_results:
#         if search_result['points'] > result['points']:
#             result = search_result
#     return result


def prioritize_link(search_results):
    # TODO: Limit the number of results
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
    return max(search_results, key=lambda single_series: single_series['points'])


def open_magnet(magnet):
    """Open magnet according to OS."""
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def download_single_season(torrents_list, chosen_series: Series, dir_path: str):
    search_result = torrents_list.search(str(chosen_series))
    while len(search_result) != 0:
        prioritized_link = prioritize_link(search_result)
        # TODO: Check MagnetLink opening to function which supports other OS
        open_magnet(prioritized_link['MagnetLink'])
        chosen_series.create_episode_path(prioritized_link['title'], dir_path)
        chosen_series.episode += 1
        chosen_series.update_episode()
        search_result = torrents_list.search(str(chosen_series))


def init_parameters():
    return Py1337x(), get_series()


def program_start(torrents: Py1337x, series: Series, dir_path=""):
    if not series.all:
        download_single_season(torrents, series, dir_path)
    else:
        search_result = torrents.search(str(series))
        series.season = 1
        while len(search_result) != 0:
            download_single_season(torrents, series, dir_path)
            series.season += 1
            series.episode = 1
            dir_path = create_series_path(series)
            search_result = torrents.search(str(series))
        exit(0)


def create_series_path(series: Series):
    season_path = series.name + '_s' + f"{series.get_season_str()}"
    user_torrent_default_path = os.path.join("D:\\", "Shows\\")
    user_dir_path = os.path.join(user_torrent_default_path, season_path)
    if not os.path.exists(user_dir_path):
        os.mkdir(user_dir_path)
    return user_torrent_default_path, user_dir_path


def main():
    db.create_database_file()
    torrents, series = init_parameters()
    series_directory, season_dir_path = create_series_path(series)
    program_start(torrents, series, season_dir_path)


if __name__ == '__main__':
    # organize_single_series("ousama ranking", "D:\\Shows\\")
    main()
