from flask import Flask, render_template, request
from os.path import abspath, dirname
import platform
import sys
from os import path
import json
import os

#messy stuff from importing from ../
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "../../", "habit-at"))
sys.path.insert(1,filepath)
from habit import Habit

#les go
client = Habit()
pathed = os.path.dirname(__file__)
path2 = os.path.dirname(pathed)
user_os = platform.system()
if user_os == "Windows":
    path = "\\"
else:
    path = "/"
app = Flask(__name__, template_folder=f"{pathed}{path}templates")

@app.route("/", methods=["GET", "POST"])
def home():
    with open(f"{path2}{path}data.json") as f:
        the_dict = json.load(f)
        f.close()
    client.get_data()
    client.is_it_ended()
    return render_template("index.html", dict_item=the_dict["habits"])

@app.route("/finish", methods=["GET", "POST"])
def finish():
    with open(f"{path2}{path}data.json") as f:
        the_dict = json.load(f)
        f.close()
    client.get_data()
    client.is_it_ended()
    return render_template("finish.html", dict_item=the_dict["habits"])

@app.route("/finish-data", methods=["POST"])
def finish_data():
    text = request.form["text-finish"]
    with open(f"{path2}{path}data.json") as f:
        the_dict = json.load(f)
        f.close()
    lists = []
    for key, value in the_dict["habits"].items():
        lists.append(key)
    if text in lists:
        if the_dict["habits"][text]["completed"]:
            client.get_data()
            client.is_it_ended()
            return render_template("error.html")
        else:
            the_dict["habits"][text]["completed"] = True
            the_dict["habits"][text]["streak"] += 1
            if the_dict["habits"][text]["streak"] > the_dict["habits"][text]["max_streak"]:
                the_dict["habits"][text]["max_streak"] = the_dict["habits"][text]["streak"]
            with open(f"{path2}{path}data.json", "w", encoding="utf-8") as f:
                json.dump(the_dict, f, ensure_ascii=False, indent=4)
                f.close()
            client.get_data()
            client.is_it_ended()
            return render_template("success.html")
    else:
        client.get_data()
        client.is_it_ended()
        return render_template("error.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    with open(f"{path2}{path}data.json") as f:
        the_dict = json.load(f)
        f.close()
    client.get_data()
    client.is_it_ended()
    return render_template("add.html", dict_item=the_dict["habits"])

@app.route("/data", methods=["POST"])
def data():
    text = request.form["text"]
    texted = text.replace(" ", "")
    text = text.strip()
    if texted == "":
        client.get_data()
        client.is_it_ended()
        return render_template("error.html")
    else:
        with open(f"{path2}{path}data.json") as f:
            new_data = json.load(f)
            f.close()
        new_data["habits"] = dict(new_data["habits"], **{text: {"streak": 0, "completed": False, "max_streak": 0}})
        with open(f'{path2}{path}data.json', "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)
                    f.close()
        client.get_data()
        client.is_it_ended()
        return render_template("success.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    with open(f"{path2}{path}data.json") as f:
        the_dict = json.load(f)
        f.close()
    client.get_data()
    client.is_it_ended()
    return render_template("delete.html", dict_item=the_dict["habits"])

@app.route("/delete-data", methods=["POST"])
def delete_data():
    text = request.form["text-finish"]
    with open(f"{path2}{path}data.json") as f:
        the_dict = json.load(f)
        f.close()
    lists = []
    for key, value in the_dict["habits"].items():
        lists.append(key)
    if text in lists:
        del the_dict["habits"][text]
        with open(f'{path2}{path}data.json', "w", encoding="utf-8") as f:
            json.dump(the_dict, f, ensure_ascii=False, indent=4)
            f.close()
        return render_template("success.html")
    else:
        return render_template("error.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    client.get_data()
    client.is_it_ended()
    return render_template("about.html")

app.run(debug=True)
