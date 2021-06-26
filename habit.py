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

script = dirname(abspath(__file__))

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
        self.script = script
        self.path = path
        self.clear = clear
        self.data = None

    def get_data(self):
        with open(f'{script}{path}data.json', "r") as f:
            data = json.load(f)
            f.close()
        self.data = data

    def check_name(self):
        self.get_data()
        if self.data["name"] is None:
            new_name = input("What is your name?\n>")
            self.data["name"] = new_name
            with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
                f.close()
                self.name = new_name
                os.system(self.clear)
        else:
            pass
            self.name = self.data["name"]

    def welcome(self):
        os.system(self.clear)
        os.system("title " + "Habit-at")
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.check_name()
        self.get_data()
        print(f"Welcome to {bcolors.OKCYAN}habit-at{bcolors.ENDC}.\n")
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
        checking = threading.Thread(target=self.is_it_end)
        checking.daemon = True
        checking.start()
        
    def is_it_end(self):
        curr = datetime.now().strftime("%m/%d/%Y")
        self.get_data()
        if self.data["timestamp"] != curr:
            for key, value in self.data["habits"].items():
                if value["completed"]:
                    value["completed"] = False
                else:
                    value["streak"] = 0
            self.data["timestamp"] = curr
            with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
                f.close()
        else:
            pass
        time.sleep(25)

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
            with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
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
            with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
                f.close()
            os.system(self.clear)
            self.welcome()
            print(f"{new_add} has been {bcolors.OKGREEN}added{bcolors.ENDC}.")

    def finish(self):
        os.system(self.clear)
        self.sep = "----------------------------------------------"
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
                with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
                    f.close()
                self.welcome()
                print(f"{bcolors.OKGREEN}{random.choice(comp)} You finished {finish}!{bcolors.ENDC}")
        else:
            os.system(self.clear)
            self.welcome()
            print("Invalid habit.")

    def del_habit(self):
        self.get_data()
        self.sep = "----------------------------------------------"
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
            with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
                    f.close()
            os.system(self.clear)
            self.welcome()
            print(f"{delete} has been {bcolors.FAIL}deleted{bcolors.ENDC}.")
        else:
            os.system(self.clear)
            self.welcome()
            print(f"{bcolors.FAIL}Invalid{bcolors.ENDC} habit.")

    def list_all(self):
        os.system(self.clear)
        self.sep = "----------------------------------------------"
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
        print(f"\n{bcolors.HEADER}{bcolors.BOLD}Press to ESC to quit.{bcolors.ENDC}")
        while True:
            if keyboard.is_pressed("esc"):
                os.system(self.clear)
                self.welcome()
                break

    def license(self):
        os.system(self.clear)
        with open(f'{self.script}{self.path}LICENSE', "r") as f:
            print(f.read())
            f.close()
        print(f"\n{bcolors.HEADER}{bcolors.BOLD}Press to ESC to quit.{bcolors.ENDC}")
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
        print(f"\n{bcolors.HEADER}{bcolors.BOLD}Press to ESC to quit.{bcolors.ENDC}")
        while True:
            if keyboard.is_pressed("esc"):
                os.system(self.clear)
                self.welcome()
                break
        

    def user_input(self):
        while True:
            user = input(f"{self.name}> ")
            user = user.strip()
            if user == "help" or user == "man" or user == "?" or user == "??" or user == "???":
                print("Documentation is at https://github.com/ultrajacobboy/habit-at")
            elif user == "add":
                self.add_habit()
            elif user == "finish":
                self.finish()
            elif user == "quit" or user == "exit":
                goodbye = ["Goodbye", "See you soon!", "Have a good day!", "See you later!"]
                curr = datetime.now().strftime("%m/%d/%Y")
                self.data["timestamp"] = curr
                with open(f'{self.script}{self.path}data.json', "w", encoding="utf-8") as f:
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
            else:
                print("Unknown command.")
