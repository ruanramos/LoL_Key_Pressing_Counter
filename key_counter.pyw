import keyboard
import mouse
import json
from collections import OrderedDict
import time
import jellyfish
import sys

champion_list = [
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

count_dict = {}
close_program = False
file_name = ""


def run():
    global champion_list
    print("Type the champion you are playing: ")
    champion = input()
    for c in champion_list:
        similarity_ratio = jellyfish.jaro_winkler(c, champion.lower().capitalize())
        if similarity_ratio <= 0.8 and similarity_ratio >= 0.7:
            print("Did you mean {}? y/n".format(c))
            answer = input()
            if answer == "y" or answer == "yes":
                treat_reactions(c)
                break
            else:
                continue
        elif similarity_ratio >= 0.85:
            treat_reactions(c)
            break
    if c == "LastElement":
        print("You typed an invalid champion, stopping the program.")
    print("bye")
    sys.exit(0)


def treat_reactions(champion):
    print("You are playing {}!".format(champion))
    keyboard.add_hotkey("ctrl+q", lambda: finish(create_file_name(champion)))
    keyboard.on_press(on_press_reaction)
    mouse.on_click(on_left_click_reaction)
    mouse.on_right_click(on_right_click_reaction)
    print(
        "Counting your actions from now on. Press ctrl+q to stop and save the history on {}_key_counter.json file.".format(
            champion
        )
    )
    while True:
        if close_program:
            break
        pass


def create_file_name(champion_name):
    return "{}_key_counter.json".format(champion_name.capitalize())


def finish(file_name):
    global close_program
    write_to_file(file_name, create_counter_json())
    close_program = True


def write_to_file(file_name, ordered_dict):
    create_counter_json()
    f = open(file_name, "a")
    t = time.localtime(time.time())
    f.write(
        "{} - {}/{}/{} - {}h:{}m:{}s\n".format(
            file_name.split("_")[0],
            t.tm_mday,
            t.tm_mon,
            t.tm_year,
            t.tm_hour,
            t.tm_min,
            t.tm_sec,
        )
    )
    json.dump(ordered_dict, f, indent=4)
    f.write("\n\n\n")
    f.close
    print("Data saved to file {}".format(file_name))


def create_counter_json():
    global count_dict
    ordered_dict = OrderedDict()
    for pair in sorted(count_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        ordered_dict[pair[0]] = pair[1]
    return ordered_dict


def on_press_reaction(event):
    global count_dict
    event_name = event.name
    if event_name in count_dict:
        count_dict[event_name] += 1
        if event_name == "s":
            print(count_dict)
    else:
        count_dict[event_name] = 1


def on_left_click_reaction():
    global count_dict
    if "left click" in count_dict:
        count_dict["left click"] += 1
    else:
        count_dict["left click"] = 1


def on_right_click_reaction():
    global count_dict
    if "right click" in count_dict:
        count_dict["right click"] += 1
    else:
        count_dict["right click"] = 1


if __name__ == "__main__":
    run()
