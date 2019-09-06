import keyboard
import mouse
import json
from collections import OrderedDict
import time
from datetime import datetime, timedelta
import jellyfish
import threading
import sys
from win32gui import GetWindowText, GetForegroundWindow, FindWindow
from apscheduler.schedulers.background import BackgroundScheduler


# TODO Check for simultaneous presses and count it

CHAMPION_LIST = [
    "Aatrox",
    "Ahri",
    "Akali",
    "Alistar",
    "Amumu",
    "Anivia",
    "Annie",
    "Ashe",
    "Aurelion Sol",
    "Azir",
    "Bard",
    "Blitzcrank",
    "Brand",
    "Braum",
    "Caitlyn",
    "Camille",
    "Cassiopeia",
    "Cho'Gath",
    "Corki",
    "Darius",
    "Diana",
    "Dr. Mundo",
    "Draven",
    "Ekko",
    "Elise",
    "Evelynn",
    "Ezreal",
    "Fiddlesticks",
    "Fiora",
    "Fizz",
    "Galio",
    "Gangplank",
    "Garen",
    "Gnar",
    "Gragas",
    "Graves",
    "Hecarim",
    "Heimerdinger",
    "Illaoi",
    "Irelia",
    "Ivern",
    "Janna",
    "Jarvan IV",
    "Jax",
    "Jayce",
    "Jhin",
    "Jinx",
    "Kai'Sa",
    "Kalista",
    "Karma",
    "Karthus",
    "Kassadin",
    "Katarina",
    "Kayle",
    "Kayn",
    "Kennen",
    "Kha'Zix",
    "Kindred",
    "Kled",
    "Kog'Maw",
    "LeBlanc",
    "Lee Sin",
    "Leona",
    "Lissandra",
    "Lucian",
    "Lulu",
    "Lux",
    "Malphite",
    "Malzahar",
    "Maokai",
    "Master Yi",
    "Miss Fortune",
    "Mordekaiser",
    "Morgana",
    "Nami",
    "Nasus",
    "Nautilus",
    "Neeko",
    "Nidalee",
    "Nocturne",
    "Nunu",
    "Olaf",
    "Orianna",
    "Ornn",
    "Pantheon",
    "Poppy",
    "Pyke",
    "Qiyana",
    "Quinn",
    "Rakan",
    "Rammus",
    "Rek'Sai",
    "Renekton",
    "Rengar",
    "Riven",
    "Rumble",
    "Ryze",
    "Sejuani",
    "Shaco",
    "Shen",
    "Shyvana",
    "Singed",
    "Sion",
    "Sivir",
    "Skarner",
    "Sona",
    "Soraka",
    "Swain",
    "Sylas",
    "Syndra",
    "Tahm Kench",
    "Tailyah",
    "Talon",
    "Taric",
    "Teemo",
    "Thresh",
    "Tristana",
    "Trundle",
    "Tryndamere",
    "Twisted Fate",
    "Twitch",
    "Udyr",
    "Urgot",
    "Varus",
    "Vayne",
    "Veigar",
    "Vel'Koz",
    "Vi",
    "Viktor",
    "Vladimir",
    "Volibear",
    "Warwick",
    "Wukong",
    "Xayah",
    "Xerath",
    "Xin Zhao",
    "Yasuo",
    "Yorick",
    "Yuumi",
    "Zac",
    "Zed",
    "Ziggs",
    "Zilean",
    "Zoe",
    "Zyra",
    "LastElement",
]

LOL_CLIENT_PROCESS_NAME = "League of Legends (TM) Client"

count_dict = {}
close_program = False
file_name = ""
start_time = ""
total_actions = 0
total_keyboard_actions = 0
total_mouse_actions = 0
actions_per_second = 0
mouse_actions_per_second = 0
keyboard_actions_per_second = 0


def get_champion_to_be_played():
    global CHAMPION_LIST
    print("Type the champion you are playing: ")
    champion = input()
    for c in CHAMPION_LIST:
        similarity_ratio = jellyfish.jaro_winkler(c, champion.lower().capitalize())
        if similarity_ratio >= 0.85:
            treat_reactions(c)
            break
        elif 0.8 >= similarity_ratio >= 0.7:
            print("Did you mean {}? y/n".format(c))
            ans = input()
            if ans == "y" or ans == "yes":
                treat_reactions(c)
                break
            else:
                continue

    if c == "LastElement":
        print("You typed an invalid champion, stopping the program.")
    print("Bye")
    sys.exit(0)


def treat_reactions(champion):
    global start_time
    print("You are playing {}!".format(champion))
    start_time = int(time.time())
    keyboard.add_hotkey("ctrl+space", lambda: finish(create_file_name(champion)))
    keyboard.on_press(on_press_reaction)
    mouse.on_click(on_left_click_reaction)
    mouse.on_right_click(on_right_click_reaction)
    print(
        "Counting your actions from now on. Press ctrl+space to stop and save the history on {}_key_counter.json file.".format(
            champion
        )
    )
    while True:
        if close_program:
            break
        if not game_happening():
            finish(create_file_name(champion))
        pass


def create_file_name(champion_name):
    return "{}_key_counter.json".format(champion_name.capitalize())


def finish(file_to_save):
    global close_program
    global start_time
    end_time = int(time.time())
    t1 = str(time.ctime(start_time))
    t2 = str(time.ctime(end_time))
    time_difference = calculate_time_difference(t1, t2)
    write_to_file(
        file_to_save,
        create_counter_json(time_difference),
        t1,
        t2,
        str(time_difference)
    )
    close_program = True


def str_time_2_seconds(time_str):
    # 0:00:00
    print(time_str)
    seconds = int(time_str[5:])
    minutes = int(time_str[2:4])
    hours = int(time_str[0:1])
    return seconds + 60 * minutes + 3600 * hours


def write_to_file(
    file_to_save, ordered_dict, start_time_to_save, end_time, time_difference
):
    create_counter_json(time_difference)
    f = open(file_to_save, "a")
    # TODO make json correct, without text
    f.write(
        "Start Recording Time: {}\nFinished Recording Time: {}\nGame Time: {}\n".format(
            start_time_to_save, end_time, time_difference
        )
    )
    json.dump(ordered_dict, f, indent=4)
    f.write("\n\n\n")
    f.close()
    print("Data saved to file {}".format(file_to_save))


def calculate_time_difference(time1, time2):
    FMT = "%H:%M:%S"
    print(time1, time2)
    tdelta = datetime.strptime(time2.split()[3], FMT) - datetime.strptime(
        time1.split()[3], FMT
    )
    if tdelta.days < 0:
        tdelta = timedelta(
            days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds
        )
    return tdelta


def create_counter_json(time_difference):
    global count_dict
    global total_actions
    global total_keyboard_actions
    global total_mouse_actions
    global mouse_actions_per_second
    global keyboard_actions_per_second
    global actions_per_second
    ordered_dict = OrderedDict()
    for pair in sorted(count_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if "click" in pair[0]:
            total_mouse_actions += pair[1]
        else:
            total_keyboard_actions += pair[1]
        total_actions += pair[1]
        ordered_dict[pair[0]] = pair[1]

    actions_per_second = total_actions / (str_time_2_seconds(str(time_difference)) + 1)
    mouse_actions_per_second = total_mouse_actions / (str_time_2_seconds(str(time_difference)) + 1)
    keyboard_actions_per_second = total_keyboard_actions / (str_time_2_seconds(str(time_difference)) + 1)
    ordered_dict["Total Mouse Actions"] = total_mouse_actions
    ordered_dict["Total Keyboard Actions"] = total_keyboard_actions
    ordered_dict["Total Actions"] = total_actions
    ordered_dict["Mouse Actions Per Second"] = mouse_actions_per_second
    ordered_dict["Keyboard Actions Per Second"] = keyboard_actions_per_second
    ordered_dict["Actions Per Second"] = actions_per_second
    return ordered_dict


def on_press_reaction(event):
    if not check_if_right_window() or not game_happening():
        return
    global count_dict
    event_name = event.name
    if event_name in count_dict:
        count_dict[event_name] += 1
        if event_name == "s":
            print(count_dict)
    else:
        count_dict[event_name] = 1


def on_left_click_reaction():
    if not check_if_right_window() or not game_happening():
        return
    global count_dict
    if "left click" in count_dict:
        count_dict["left click"] += 1
    else:
        count_dict["left click"] = 1


def on_right_click_reaction():
    if not check_if_right_window() or not game_happening():
        return
    global count_dict
    if "right click" in count_dict:
        count_dict["right click"] += 1
    else:
        count_dict["right click"] = 1


def check_if_right_window():
    global LOL_CLIENT_PROCESS_NAME
    return LOL_CLIENT_PROCESS_NAME == GetWindowText(GetForegroundWindow())


def game_happening():
    global LOL_CLIENT_PROCESS_NAME
    return GetWindowText(FindWindow(None, LOL_CLIENT_PROCESS_NAME)) != ""


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        while not game_happening():
            print(
                "There is no game happening or game window is closed. Want to try again? y/n"
            )
            answer = input()
            if answer == "y" or answer == "yes":
                continue
            else:
                sys.exit(0)
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_if_right_window, "interval", seconds=0.5)
    scheduler.start()
    try:
        get_champion_to_be_played()
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
