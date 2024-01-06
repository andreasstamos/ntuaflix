from functools import wraps
from pathlib import Path
import typer
import json
from rich import print
from rich.table import Table
import io
import csv

from config import *

from enum import Enum

class Format(str, Enum):
    json = "json"
    csv = "csv"

def load_config(var):
    app_dir = Path(typer.get_app_dir(APP_NAME))
    config_path = app_dir / "config.json"
    if config_path.is_file():
        try:
            with open(config_path, "r") as config_f:
                config = json.load(config_f)
            if var in config:
                return config[var]
        except: pass
    else:
        print("doesnt exist")
    return None

def store_config(var, value):
    app_dir = Path(typer.get_app_dir(APP_NAME))
    config_path = app_dir / "config.json"
    config = {}
    if config_path.is_file():
        try:
            with open(config_path, "r") as config_f:
                config = json.load(config_f)
        except: pass
    
    if value is not None: config[var] = value
    else:
        config.pop(var, None)

    app_dir.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as config_f:
        json.dump(config, config_f)

def call_inject_variable(func, variables, args, kwargs):
    sentinels = [object() for _ in range(len(variables))]
    olds = [func.__globals__.get(name, sentinel) for name, sentinel in zip(variables.keys(), sentinels)]
    func.__globals__.update(variables)
    ret = func(*args, **kwargs)
    for name, old, sentinel in zip(variables.keys(), olds, sentinels):
        if old is sentinel: func.__globals__.pop(name)
        else: func.__globals__[name] = old
    return ret

def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = load_config("api_key")
        if api_key is not None:
            return call_inject_variable(func, {'api_key':api_key}, args, kwargs)
        else:
            print(":locked_with_key: [bold red]You are not authenticated. Please login first.[/bold red]")
    return wrapper

def handle_request(path, payload=None, api_key=None, parse_json=False):
    try:
        response = requests.post(API_URL + path,
                **({'headers': {"X-OBSERVATORY-AUTH": api_key}} if api_key is not None else {}),
                **({'payload': payload} if payload is not None else {}),
                    )
        if response.status_code == 200:
            return response.json() if parse_json else response
        else:
            print(":no_good: [bold red]Server responded in an irregular manner (bad status code). Please contact system administrator.[/bold red]")
    except requests.ConnectionError:
        print(":cross_mark: [bright_black]Server is down.[/bright_black]")
    except requests.JSONDecodeError:
        print(":no_good: [bold red]Server responded in an irregular manner (bad JSON). Please contact system administrator.[/bold red]")
    return None

def print_csv(text):
    csv_data = io.StringIO(text)
    csv_reader = csv.reader(csv_data)
    table = Table()
    try:
        headers = next(csv_reader)
        for header in headers:
            table.add_column(header)
        for row in csv_reader:
            table.add_row(*row)
    except csv.Error:
        print(":no_good: [bold red]Server responded in an irregular manner (bad CSV). Please contact system administrator.[/bold red]")
        return
    print(table)

