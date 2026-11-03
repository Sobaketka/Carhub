import os
import argparse
import sys
import functions
import commands


def repl():
    cars = functions.get_cars()

    print("CarHub")
    print("Команди: help - список команд")

    while True:
        user_action = input("--> ")
        if commands.dispatch(cars, user_action) is False:
            break

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python interdod1.py",
        description="Cars: діалог або команда під час запуску."
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("show", help="Показати список")

    p_add = sub.add_parser("add", help="Додати автомобіль")
    p_add.add_argument(
        "text", nargs="+",
        help="Дані автомобіля (марка, модель, рік, ціна, пробіг)"
    )

    p_edit = sub.add_parser("edit", help="Редагувати автомобіль")
    p_edit.add_argument("number", type=int, help="Номер автомобіля")
    p_edit.add_argument("data", nargs="+", help="Нові дані автомобіля")

    p_delete = sub.add_parser("delete", help="Видалити автомобіль")
    p_delete.add_argument("number", type=int, help="Номер автомобіля")

    p_search = sub.add_parser("search", help="Пошук за маркою")
    p_search.add_argument("brand", help="Марка автомобіля")

    p_sold = sub.add_parser("sold", help="Змінити статус автомобіля")
    p_sold.add_argument("number", type=int, help="Номер автомобіля")

    p_filter = sub.add_parser("filter", help="Фільтр за статусом")
    p_filter.add_argument("choice", choices=["1", "2"])

    p_info = sub.add_parser("info", help="Інформація про автомобіль")
    p_info.add_argument("number", type=int, help="Номер автомобіля")

    p_range = sub.add_parser("range", help="Пошук за діапазоном цін")
    p_range.add_argument("low", type=int, help="Мінімальна ціна")
    p_range.add_argument("high", type=int, help="Максимальна ціна")

    p_discount = sub.add_parser("discount", help="Знижка на автомобіль")
    p_discount.add_argument("number", type=int, help="Номер автомобіля")
    p_discount.add_argument("percent", type=int, help="Відсоток знижки")

    sub.add_parser("sort", help="Сортувати за ціною")
    sub.add_parser("brands", help="Кількість автомобілів кожної марки")
    sub.add_parser("stats", help="Статистика")
    sub.add_parser("clear", help="Видалити всі автомобілі")
    sub.add_parser("help", help="Список команд")
    sub.add_parser("repl", help="Почати діалог")

    return parser

def run_from_args(args):

    if args.command == "repl":
        repl()
        return

    cars = functions.get_cars()

    if args.command == "add":
        text = " ".join(args.text)
        commands.dispatch(cars, f"add {text}")

    elif args.command == "show":
        commands.dispatch(cars, "show")

    elif args.command == "edit":
        data = " ".join(args.data)
        commands.dispatch(cars, f"edit {args.number} {data}")

    elif args.command == "delete":
        commands.dispatch(cars, f"delete {args.number}")

    elif args.command == "search":
        commands.dispatch(cars, f"search {args.brand}")

    elif args.command == "sold":
        commands.dispatch(cars, f"sold {args.number}")

    elif args.command == "filter":
        commands.dispatch(cars, f"filter {args.choice}")

    elif args.command == "info":
        commands.dispatch(cars, f"info {args.number}")

    elif args.command == "range":
        commands.dispatch(cars, f"range {args.low} {args.high}")

    elif args.command == "discount":
        commands.dispatch(cars, f"discount {args.number} {args.percent}")

    elif args.command == "sort":
        commands.dispatch(cars, "sort")

    elif args.command == "brands":
        commands.dispatch(cars, "brands")

    elif args.command == "stats":
        commands.dispatch(cars, "stats")

    elif args.command == "clear":
        commands.dispatch(cars, "clear")

    elif args.command == "help":
        commands.dispatch(cars, "help")


def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(functions.FILEPATH):
        with open(functions.FILEPATH, "w", encoding="utf-8"):
            pass

    if len(sys.argv) == 1:
        repl()
        return

    parser = build_parser()
    args = parser.parse_args()
    run_from_args(args)


if __name__ == "__main__":
    main()
    print("Кінець!")