import keyboard

count_dict = {}


def on_press_reaction(event):
    global count_dict
    event_name = event.name
    if event_name in count_dict:
        count_dict[event_name] += 1
        if event_name == "s":
            print(count_dict)
    else:
        count_dict[event_name] = 1


if __name__ == "__main__":
    keyboard.on_press(on_press_reaction)
    while True:
        pass
