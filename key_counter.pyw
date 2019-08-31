import keyboard
import json
from collections import OrderedDict
from tkinter import *
import threading
import time


count_dict = {}
close_program = False


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.champion_name = StringVar(self.master, value="Leblanc")
        champions = {"Leblanc", "Fizz", "Ahri", "Aatrox", "Irelia"}
        self.champion_name.set("Leblanc")  # set the default option
        self.popupMenu = OptionMenu(self.master, self.champion_name, *champions)

        self.start_button = Button(self)
        self.start_button["text"] = "Confirm Champion"
        self.start_button["command"] = lambda: self.get_champion(self.champion_name)

        self.quit = Button(
            self,
            text="QUIT AND SAVE RESULT",
            fg="red",
            command=lambda: [finish(), self.master.destroy()],
        )

        # packing
        self.start_button.pack()
        self.quit.pack()
        self.popupMenu.pack()

    # on change dropdown value
    def change_dropdown(self, champion_name, *args):
        return champion_name.get()

    def get_champion(self, champion_name):
        # link function to change dropdown
        self.champion_name.trace("w", lambda: self.change_dropdown(self.champion_name))
        print(champion_name)


class TkThread(threading.Thread):
    def run(self):
        print("{} started!".format(self.getName()))  # "Thread-x started!"
        root = Tk()
        app = Application(master=root)
        app.mainloop()


class CounterThread(threading.Thread):
    def run(self):
        print("{} started!".format(self.getName()))  # "Thread-x started!"
        run()


def on_press_reaction(event):
    global count_dict
    event_name = event.name
    if event_name in count_dict:
        count_dict[event_name] += 1
        if event_name == "s":
            print(count_dict)
    else:
        count_dict[event_name] = 1


def finish():
    global count_dict
    global close_program
    ordered_dict = OrderedDict()
    f = open("keys_pressed.txt", "w")
    for pair in sorted(count_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        ordered_dict[pair[0]] = pair[1]
    json.dump(ordered_dict, f, indent=4)
    f.close
    close_program = True


def run():
    keyboard.add_hotkey("ctrl+q", finish)
    keyboard.on_press(on_press_reaction)
    while True:
        if close_program:
            break
        pass


if __name__ == "__main__":
    tkThread = TkThread(name="TkThread")
    counterThread = CounterThread(name="CounterThread")
    tkThread.start()
    counterThread.start()
