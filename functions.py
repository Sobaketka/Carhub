import json
import os

FILEPATH = os.path.join("data", "cars.json")


def get_cars(filepath = FILEPATH):
    with open(filepath, "r", encoding="utf-8") as file:
        if os.path.getsize(filepath) == 0:
            return []
        return json.load(file)


def write_cars(cars_arg, filepath = FILEPATH):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(cars_arg, file, ensure_ascii=False, indent=4)


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

if __name__ == "__main__":
    cars = get_cars(FILEPATH)
    print(cars)