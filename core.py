import shutil
from datetime import datetime
from pathlib import Path
import functions


def add_car(cars, car):
    cars.append(car)
    functions.write_cars(cars)


def edit_car(cars, number, car):
    if number < 1 or number > len(cars):
        raise IndexError
    car["sold"] = cars[number - 1]["sold"]
    cars[number - 1] = car
    functions.write_cars(cars)


def delete_car(cars, number):
    if number < 1 or number > len(cars):
        raise IndexError
    cars.pop(number - 1)
    functions.write_cars(cars)


def change_sold(cars, number):
    if number < 1 or number > len(cars):
        raise IndexError
    cars[number - 1]["sold"] = not cars[number - 1]["sold"]
    functions.write_cars(cars)

def clear_cars(cars):
    cars.clear()
    functions.write_cars(cars)


def backup_todos(filepath=functions.FILEPATH):
    source = Path(filepath)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = source.with_name(f"{source.stem}-backup-{timestamp}{source.suffix}")
    shutil.copy2(source, backup)
    return backup