import json
import os

FILEPATH = os.path.join("data", "cars.json")


def load_cars():
    if os.path.getsize(FILEPATH) == 0:
        return []
    with open(FILEPATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cars(cars):
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(cars, file, ensure_ascii=False, indent=4)


def print_car(number, car):
    if car["sold"]:
        status = "ПРОДАНО"
    else:
        status = "в наявності"
    print(number, "->", car["brand"], car["model"], "-", car["year"], "рік -",
          car["price"], "$ -", car["mileage"], "км [" + status + "]")


def ask_number(cars):
    text = input("> ")
    if not text.isdigit():
        print("Номер повинен бути числом")
        return 0
    number = int(text)
    if number < 1 or number > len(cars):
        print("Такої машини немає")
        return 0
    return number