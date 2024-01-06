from functools import wraps
from pathlib import Path
import typer
import json
from rich import print

from config import *

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

