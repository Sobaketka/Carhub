import os
import argparse
import sys
import functions
import commands
import click
import typer



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

    p_edit = sub.add_parser("edit", help="Редагувати автомобіль (введіть: Марка, модель, рік, ціна, пробіг)")
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
    sub.add_parser("backup", help ="Створити резервну копію")
    sub.add_parser("repl", help="Запустити діалог")

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

@click.group(help="Те саме через Click")
def click_cli():
    pass

@click_cli.command("show")
def click_show():
    commands.dispatch(functions.get_cars(), "show")

@click_cli.command("add")
@click.argument("text", nargs=-1, required=True)
def click_add(text):
    text = " ".join(text)
    commands.dispatch(functions.get_cars(), f"add {text}")

@click_cli.command("edit")
@click.argument("number", type=int)
@click.argument("data", nargs=-1, required=True)
def click_edit(number, data):
    data = " ".join(data)
    commands.dispatch(functions.get_cars(), f"edit {number} {data}")

@click_cli.command("delete")
@click.argument("number", type=int)
def click_delete(number):
    commands.dispatch(functions.get_cars(), f"delete {number}")

@click_cli.command("search")
@click.argument("brand", type=str)
def click_search(brand):
    commands.dispatch(functions.get_cars(), f"search {brand}")

@click_cli.command("sold")
@click.argument("number", type=int)
def click_sold(number):
    commands.dispatch(functions.get_cars(), f"sold {number}")

@click_cli.command("filter")
@click.argument("choice", type=click.Choice(["1", "2"]))
def click_filter(choice):
    commands.dispatch(functions.get_cars(), f"filter {choice}")

@click_cli.command("info")
@click.argument("number", type=int)
def click_info(number):
    commands.dispatch(functions.get_cars(), f"info {number}")

@click_cli.command("range")
@click.argument("low", type=int)
@click.argument("high", type=int)
def click_range(low, high):
    commands.dispatch(functions.get_cars(), f"range {low} {high}")

@click_cli.command("discount")
@click.argument("number", type=int)
@click.argument("percent", type=int)
def click_discount(number, percent):
    commands.dispatch(functions.get_cars(), f"discount {number} {percent}")

@click_cli.command("sort")
def click_sort():
    commands.dispatch(functions.get_cars(), "sort")

@click_cli.command("brands")
def click_brands():
    commands.dispatch(functions.get_cars(), "brands")

@click_cli.command("stats")
def click_stats():
    commands.dispatch(functions.get_cars(), "stats")

@click_cli.command("clear")
def click_clear():
    commands.dispatch(functions.get_cars(), "clear")

@click_cli.command("help")
def click_help():
    commands.dispatch(functions.get_cars(), "help")

@click_cli.command("backup")
def click_backup():
    commands.dispatch(functions.get_cars(), "backup")

@click_cli.command("repl")
def click_repl():
    repl()


typer_app = typer.Typer(help = "Те саме через Typer")

@typer_app.command("show")
def typer_show():
    commands.dispatch(functions.get_cars(), "show")

@typer_app.command("add")
def typer_add(text: list[str] = typer.Argument(..., help="Марка, модель, рік, ціна, пробіг")):
    text = " ".join(text)
    commands.dispatch(functions.get_cars(), f"add {text}")

@typer_app.command("edit")
def typer_edit(
    number: int,
    data: list[str] = typer.Argument(..., help="Нові дані автомобіля"),
):
    data = " ".join(data)
    commands.dispatch(functions.get_cars(), f"edit {number} {data}")

@typer_app.command("delete")
def typer_delete(number: int):
    commands.dispatch(functions.get_cars(), f"delete {number}")

@typer_app.command("search")
def typer_search(brand: str):
    commands.dispatch(functions.get_cars(), f"search {brand}")

@typer_app.command("sold")
def typer_sold(number: int):
    commands.dispatch(functions.get_cars(), f"sold {number}")

@typer_app.command("filter")
def typer_filter(choice: str):
    if choice not in ("1", "2"):
        raise typer.BadParameter("Оберіть 1 або 2")
    commands.dispatch(functions.get_cars(), f"filter {choice}")

@typer_app.command("info")
def typer_info(number: int):
    commands.dispatch(functions.get_cars(), f"info {number}")

@typer_app.command("range")
def typer_range(low: int, high: int):
    commands.dispatch(functions.get_cars(), f"range {low} {high}")

@typer_app.command("discount")
def typer_discount(number: int, percent: int):
    commands.dispatch(functions.get_cars(), f"discount {number} {percent}")

@typer_app.command("sort")
def typer_sort():
    commands.dispatch(functions.get_cars(), "sort")

@typer_app.command("brands")
def typer_brands():
    commands.dispatch(functions.get_cars(), "brands")

@typer_app.command("stats")
def typer_stats():
    commands.dispatch(functions.get_cars(), "stats")

@typer_app.command("clear")
def typer_clear():
    commands.dispatch(functions.get_cars(), "clear")

@typer_app.command("help")
def typer_help():
    commands.dispatch(functions.get_cars(), "help")

@typer_app.command("backup")
def typer_backup():
    commands.dispatch(functions.get_cars(), "backup")

@typer_app.command("repl")
def typer_repl():
    repl()


def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(functions.FILEPATH):
        with open(functions.FILEPATH, "w", encoding="utf-8"):
            pass

    if len(sys.argv) == 1:
        repl()
        return

    if sys.argv[1] == "click":
        click_cli(args = sys.argv[2:], prog_name = "python interdod1.py click")
        return

    if sys.argv[1] == "typer":
        typer_app(args = sys.argv[2:], prog_name = "python interdod1.py typer")
        return

    parser = build_parser()
    args = parser.parse_args()
    run_from_args(args)

if __name__ == "__main__":
    main()
    print("Кінець!")