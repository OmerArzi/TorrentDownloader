import os
import shutil
import sys
import subprocess
import WatchStatusDBM as db


def get_file_names_with_strings(name_contains_list: list, path: str):
    full_list = os.listdir(path)
    flag = True
    for file_in_directory in full_list:
        lower_file_in_directory = file_in_directory.lower()
        if all(sub_string in lower_file_in_directory for sub_string in name_contains_list):
            return file_in_directory
    return False


def get_relevant_file_name(episode: list, series_directory: str):
    current_file_path = os.path.join(series_directory, episode[3])
    episode_separated_name = episode[0].split(' ')
    if not os.path.exists(current_file_path):
        season_str = "s0" + str(episode[1]) if episode[1] < 10 else "s" + str(episode[1])
        episode_str = "e0" + str(episode[2]) if episode[2] < 10 else "e" + str(episode[2])
        arg_list = [word for word in episode_separated_name] + [season_str, episode_str]
        current_file_path = get_file_names_with_strings(arg_list, series_directory)
        return current_file_path if current_file_path else False


def organize_single_series(series_name: str, series_directory: str):
    conn = db.init_database()
    episodes_list = db.select_episodes_by_name(conn, series_name)
    for episode in episodes_list:
        current_file_name = get_relevant_file_name(episode, series_directory)
        if current_file_name and os.path.exists(series_directory):
            current_file_path = os.path.join(series_directory, current_file_name)
            destination_path = os.path.join(episode[4], current_file_name)
            shutil.move(current_file_path, destination_path)
        # ensure the destined path exists.
        # move it to destined path
        # update location
        pass
