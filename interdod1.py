import os
import functions
import commands


def repl():
    cars = functions.load_cars()

    print("CarHub")
    print("Команди: help - список команд")

    while True:
        command = input("--> ")
        if not commands.dispatch(cars, command):
            break


def main():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(functions.FILEPATH):
        with open(functions.FILEPATH, "w", encoding="utf-8"):
            pass

    repl()


if __name__ == "__main__":
    main()
    print("Кінець!")