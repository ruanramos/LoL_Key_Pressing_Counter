import keyboard

# with open("read_event.txt", "w") as f1, open("read_key.txt", "w") as f2:
#     while True:
#         f1.write(str(keyboard.read_event()))
#         f1.write(" ")

# def addCount(key):

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
