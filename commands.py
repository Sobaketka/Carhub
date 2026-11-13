import functions
import core

def do_help(cars, argument):
    print("add      - додати машину")
    print("show     - показати всі машини")
    print("edit     - змінити машину")
    print("delete   - видалити машину")
    print("search   - пошук за маркою")
    print("sold     - змінити статус продано / не продано")
    print("filter   - показати тільки в наявності або тільки продані")
    print("info     - інформація про одну машину")
    print("range    - пошук за діапазоном цін")
    print("discount - знижка на машину у відсотках")
    print("sort     - сортувати за ціною")
    print("brands   - скільки машин кожної марки")
    print("stats    - статистика")
    print("clear    - видалити всі машини")
    print("exit     - вихід")


def do_add(cars, argument):
    if not argument:
        print("Вкажіть: марка модель рік ціна пробіг")
        argument = input("> ")
    data = argument.split()

    if len(data) == 5 and data[2].isdigit() and data[3].isdigit() and data[4].isdigit():
        car = {
            "brand": data[0],
            "model": data[1],
            "year": int(data[2]),
            "price": int(data[3]),
            "mileage": int(data[4]),
            "sold": False
        }
        core.add_car(cars, car)
        print("Машину додано")
    else:
        print("Неправильні дані")


def do_show(cars, argument):
    if len(cars) == 0:
        print("Список машин порожній")
    else:
        for i in range(len(cars)):
            functions.print_car(i + 1, cars[i])


def do_delete(cars, argument):
    if not argument:
        print("Вкажіть номер машини")
        argument = input("> ")

    if argument.isdigit():
        number = int(argument)

        if 1 <= number <= len(cars):
            core.delete_car(cars, number)
            print("Машину видалено")
        else:
            print("Такої машини немає")
    else:
        print("Номер повинен бути числом")


def do_search(cars, argument):
    if not argument:
        print("Вкажіть марку")
        argument = input("> ")

    found = False

    for i in range(len(cars)):
        if cars[i]["brand"].lower() == argument.lower():
            functions.print_car(i + 1, cars[i])
            found = True

    if not found:
        print("Машину не знайдено")


def do_edit(cars, argument):
    if not argument:
        print("Вкажіть: номер марка модель рік ціна пробіг")
        argument = input("> ")
    data = argument.split()

    if len(data) == 6 and data[0].isdigit() and data[3].isdigit() and data[4].isdigit() and data[5].isdigit():
        number = int(data[0])

        if 1 <= number <= len(cars):
            car = {
                "brand": data[1],
                "model": data[2],
                "year": int(data[3]),
                "price": int(data[4]),
                "mileage": int(data[5])
            }

            core.edit_car(cars, number, car)
            print("Машину змінено")
        else:
            print("Такої машини немає")
    else:
        print("Неправильні дані")


def do_sold(cars, argument):
    if not argument:
        print("Вкажіть номер машини")
        argument = input("> ")

    if argument.isdigit():
        number = int(argument)

        if 1 <= number <= len(cars):
            core.change_sold(cars, number)

            if cars[number - 1]["sold"]:
                print("Статус: продано")
            else:
                print("Статус: в наявності")
        else:
            print("Такої машини немає")
    else:
        print("Номер повинен бути числом")


def do_filter(cars, argument):
    if not argument:
        print("1 - в наявності, 2 - продані")
        argument = input("> ")

    if argument == "1" or argument == "2":
        found = False

        for i in range(len(cars)):
            if argument == "1" and not cars[i]["sold"]:
                functions.print_car(i + 1, cars[i])
                found = True
            elif argument == "2" and cars[i]["sold"]:
                functions.print_car(i + 1, cars[i])
                found = True

        if not found:
            print("Нічого не знайдено")
    else:
        print("Неправильний вибір")




def do_info(cars, argument):
    if not argument:
        print("Вкажіть номер машини")
        argument = input("> ")

    if argument.isdigit():
        number = int(argument)

        if 1 <= number <= len(cars):
            car = cars[number - 1]

            print("Марка:", car["brand"])
            print("Модель:", car["model"])
            print("Рік:", car["year"])
            print("Ціна:", car["price"], "$")
            print("Пробіг:", car["mileage"], "км")

            if car["sold"]:
                print("Статус: продано")
            else:
                print("Статус: в наявності")
        else:
            print("Такої машини немає")
    else:
        print("Номер повинен бути числом")


def do_range(cars, argument):
    if not argument:
        print("Вкажіть діапазон цін: від до")
        argument = input("> ")

    data = argument.split()

    if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
        low = int(data[0])
        high = int(data[1])

        found = False

        for i in range(len(cars)):
            if low <= cars[i]["price"] <= high:
                functions.print_car(i + 1, cars[i])
                found = True

        if not found:
            print("Нічого не знайдено")
    else:
        print("Неправильні дані")


def do_discount(cars, argument):
    if not argument:
        print("Вкажіть: номер знижка(%)")
        argument = input("> ")

    data = argument.split()

    if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
        number = int(data[0])
        percent = int(data[1])

        if number < 1 or number > len(cars):
            print("Такої машини немає")
        elif percent < 1 or percent > 99:
            print("Знижка має бути від 1 до 99")
        elif cars[number - 1]["sold"]:
            print("Ця машина вже продана")
        else:
            old_price = cars[number - 1]["price"]
            new_price = old_price * (100 - percent) // 100
            cars[number - 1]["price"] = new_price

            functions.write_cars(cars)
            print("Ціна:", old_price, "$ ->", new_price, "$")
    else:
        print("Неправильні дані")


def do_sort(cars, argument):
    for i in range(len(cars)):
        for j in range(len(cars) - 1 - i):
            if cars[j]["price"] > cars[j + 1]["price"]:
                cars[j], cars[j + 1] = cars[j + 1], cars[j]

    functions.write_cars(cars)
    print("Відсортовано за ціною")


def do_brands(cars, argument):
    counts = {}

    for car in cars:
        brand = car["brand"]

        if brand in counts:
            counts[brand] += 1
        else:
            counts[brand] = 1

    if len(counts) == 0:
        print("Список машин порожній")
    else:
        for brand in counts:
            print(brand, "-", counts[brand])


def do_stats(cars, argument):
    if len(cars) == 0:
        print("Список машин порожній")
    else:
        sold_count = 0
        total_price = 0
        sold_sum = 0

        for car in cars:
            total_price += car["price"]

            if car["sold"]:
                sold_count += 1
                sold_sum += car["price"]

        print("Всього машин:", len(cars))
        print("Продано:", sold_count)
        print("В наявності:", len(cars) - sold_count)
        print("Середня ціна:", total_price // len(cars), "$")
        print("Сума продажів:", sold_sum, "$")


def do_clear(cars, argument):
    if not argument:
        argument = input("Точно видалити все? (y/n) > ")

    if argument == "y":
        core.clear_cars(cars)
        print("Всі машини видалено")

def do_exit(cars, argument):
    functions.write_cars(cars)
    print("Збережено")
    return False

COMMANDS = {
    "help": do_help,
    "add": do_add,
    "show": do_show,
    "edit": do_edit,
    "delete": do_delete,
    "search": do_search,
    "sold": do_sold,
    "filter": do_filter,
    "info": do_info,
    "range": do_range,
    "discount": do_discount,
    "sort": do_sort,
    "brands": do_brands,
    "stats": do_stats,
    "clear": do_clear,
    "exit": do_exit,
}


def dispatch(cars, user_action):
    parts = user_action.strip().split(maxsplit=1)

    if not parts:
        print("Введіть команду")
        return True

    command = parts[0]
    argument = parts[1] if len(parts) > 1 else ""
    handler = COMMANDS.get(command)

    if handler is None:
        print("Невідома команда (help - список команд)")
        return True

    return handler(cars, argument)