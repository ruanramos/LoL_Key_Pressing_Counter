import keyboard
import mouse
import json
from collections import OrderedDict

count_dict = {}
close_program = False


def run():
    keyboard.add_hotkey("ctrl+q", finish)
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


def finish():
    global count_dict
    global close_program
    ordered_dict = OrderedDict()
    f = open("keys_pressed.json", "w")
    for pair in sorted(count_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        ordered_dict[pair[0]] = pair[1]
    json.dump(ordered_dict, f, indent=4)
    f.close
    close_program = True


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
