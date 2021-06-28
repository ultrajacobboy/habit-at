from datetime import datetime
import time
from os.path import abspath, dirname
import platform
import json
import os
import sys
import keyboard
import threading
import random
from os import path

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "data.json"))

user_os = platform.system()
if user_os == "Windows":
    path = "\\"
    clear = "cls"
else:
    path = "/"
    clear = "clear"

class bcolors:
    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    # I didn't want to use colorama; as it is an external module
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Habit:

    def __init__(self):
        self.path = path
        self.clear = clear
        self.data = None
        self.sep = "----------------------------------------------"

    def get_data(self):
        with open(f'{filepath}', "r") as f:
            self.data = json.load(f)
            f.close()

    def welcome(self):
        os.system(self.clear)
        os.system("title " + "Habit-at")
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.get_data()
        self.name = self.data["name"]
        print(f"Welcome to {bcolors.OKCYAN}habit-at lightweight{bcolors.ENDC}.\n")
        print(f"It is currently {bcolors.OKCYAN}{date_time}{bcolors.ENDC}")
        hab_num = 0
        for i in self.data["habits"]:
            hab_num += 1
        if hab_num == 0:
            print(f"You are currently tracking {bcolors.FAIL}{hab_num}{bcolors.ENDC} habits.\n")
        elif hab_num == 1:
            print(f"You are currently tracking {bcolors.OKGREEN}{hab_num}{bcolors.ENDC} habit.\n")
        else:
            print(f"You are currently tracking {bcolors.OKGREEN}{hab_num}{bcolors.ENDC} habits.\n")
        print("* Github: https://github.com/ultrajacobboy/habit-at")
        self.is_it_ended()

    def is_it_ended(self):
        curr = datetime.now().strftime("%m/%d/%Y")
        self.get_data()
        if self.data["timestamp"] != curr:
            for key, value in self.data["habits"].items():
                if value["completed"]:
                    value["completed"] = False
                else:
                    value["streak"] = 0
            self.data["timestamp"] = curr
            with open(f'{filepath}', "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
                f.close()
        else:
            pass

    def add_habit(self):
        os.system(self.clear)
        add = input("Enter the name of the habit\n> ")
        new_added = add.replace(" ", "")
        new_add = add.strip()
        if new_added == "":
            os.system(self.clear)
            self.welcome()
            print("Invalid name.")
            return
        else:
            self.get_data()
            new_data = self.data
            new_data["habits"] = dict(self.data["habits"], **{new_add: {"streak": 0, "completed": False, "max_streak": 0}})
            with open(f'{filepath}', "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
                f.close()
            os.system(self.clear)
            self.welcome()
            print(f"{new_add} has been {bcolors.OKGREEN}added{bcolors.ENDC}.")
            self.is_it_ended()

    def finish(self):
        os.system(self.clear)
        self.get_data()
        lists = []
        for key, value in self.data["habits"].items():
            if value["completed"]:
                print(f"{key} {bcolors.OKGREEN}Completed{bcolors.ENDC}, Streak: {value['streak']}, Max Streak: {value['max_streak']}")
                print(self.sep)
            else:
                print(f"{key} {bcolors.FAIL}NOT completed{bcolors.ENDC}, Streak: {value['streak']}, Max Streak: {value['max_streak']}")
                print(self.sep)
            lists.append(key)
        finish = input("Which activity have you finished?\n> ")
        if finish in lists:
            if self.data["habits"][finish]["completed"]:
                os.system(self.clear)
                print(f"{bcolors.FAIL}Already finished for today!{bcolors.ENDC}")
                return
            else:
                os.system(self.clear)
                comp = ["Great job!", "Keep it up!", "Amazing!"]
                self.data["habits"][finish]["completed"] = True
                self.data["habits"][finish]["streak"] += 1
                if self.data["habits"][finish]["streak"] > self.data["habits"][finish]["max_streak"]:
                    self.data["habits"][finish]["max_streak"] = self.data["habits"][finish]["streak"]
                with open(f'{filepath}', "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
                    f.close()
                self.welcome()
                print(f"{bcolors.OKGREEN}{random.choice(comp)} You finished {finish}!{bcolors.ENDC}")
                self.is_it_ended()
        else:
            os.system(self.clear)
            self.welcome()
            print("Invalid habit.")
            self.is_it_ended()

    def del_habit(self):
        self.get_data()
        os.system(self.clear)
        lists = []
        for key, value in self.data["habits"].items():
            if value["completed"]:
                print(f"{key} {bcolors.OKGREEN}Completed{bcolors.ENDC}, Streak: {value['streak']}, Max Streak: {value['max_streak']}")
                print(self.sep)
            else:
                print(f"{key} {bcolors.FAIL}NOT completed{bcolors.ENDC}, Streak: {value['streak']}, Max Streak: {value['max_streak']}")
                print(self.sep)
            lists.append(key)
        delete = input(f"Enter the name of the habit you want to {bcolors.FAIL}delete{bcolors.ENDC}\n> ")
        if delete in lists:
            del self.data["habits"][delete]
            with open(f'{filepath}', "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
                    f.close()
            os.system(self.clear)
            self.welcome()
            print(f"{delete} has been {bcolors.FAIL}deleted{bcolors.ENDC}.")
            self.is_it_ended()
        else:
            os.system(self.clear)
            self.welcome()
            print(f"{bcolors.FAIL}Invalid{bcolors.ENDC} habit.")
            self.is_it_ended()

    def list_all(self):
        os.system(self.clear)
        self.get_data()
        lists = []
        m = 0
        for key, value in self.data["habits"].items():
            if value["completed"]:
                print(f"{key} {bcolors.OKGREEN}Completed{bcolors.ENDC}, Streak: {value['streak']}, Max Streak: {value['max_streak']}")
                print(self.sep)
            else:
                print(f"{key} {bcolors.FAIL}NOT completed{bcolors.ENDC}, Streak: {value['streak']}, Max Streak: {value['max_streak']}")
                print(self.sep)
            m += 1
        print(f"You have {m} habits")
        print(self.sep)
        print(f"\n{bcolors.HEADER}{bcolors.BOLD}Press to ESC to exit.{bcolors.ENDC}")
        self.is_it_ended()
        while True:
            if keyboard.is_pressed("esc"):
                os.system(self.clear)
                self.welcome()
                break

    def system(self):
        os.system(self.clear)
        print(f"Platform: {platform.system()}")
        print(f"Release: {platform.release()}")
        print(f"Version: {platform.version()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Processor: {platform.processor()}")
        print(f"\n{bcolors.HEADER}{bcolors.BOLD}Press to ESC to exit.{bcolors.ENDC}")
        self.is_it_ended()
        while True:
            if keyboard.is_pressed("esc"):
                os.system(self.clear)
                self.welcome()
                break

    def stopwatch(self):
        os.system(self.clear)
        start_time = datetime.now()
        self.is_it_ended()
        while True:
            if keyboard.is_pressed("esc"):
                os.system(self.clear)
                self.welcome()
                break
            else:
                time_rn = datetime.now()
                print(time_rn - start_time)
                print(f"\n{bcolors.HEADER}{bcolors.BOLD}Press to ESC to exit.{bcolors.ENDC}")
                os.system(self.clear)

    def user_input(self):
        while True:
            user = input(f"lightweight> ").strip().lower()
            #user = user.strip()
            if user == "help" or user == "man" or user == "?" or user == "??" or user == "???":
                print("Documentation is at https://github.com/ultrajacobboy/habit-at")
            elif user == "add":
                self.add_habit()
            elif user == "finish":
                self.finish()
            elif user == "quit" or user == "exit" or user == "bye":
                goodbye = ["Goodbye", "See you soon!", "Have a good day!", "See you later!"]
                curr = datetime.now().strftime("%m/%d/%Y")
                self.data["timestamp"] = curr
                with open(f'{filepath}', "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
                    f.close()
                os.system(self.clear)
                print(f"{bcolors.OKGREEN}{random.choice(goodbye)}{bcolors.ENDC}")
                sys.exit()
            elif user == "":
                pass
            elif user == "license":
                self.license()
            elif user == "delete" or user == "del":
                self.del_habit()
            elif user == "list_all" or user == "list all" or user == "list":
                self.list_all()
            elif user == "system":
                self.system()
            elif user == "stopwatch":
                self.stopwatch()
            else:
                os.system(self.clear)
                self.welcome()
                print(f"{bcolors.FAIL}Unknown command.{bcolors.ENDC}")