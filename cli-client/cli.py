from typing_extensions import Annotated
import typer
from rich import print, print_json
import requests

from utils import load_config, store_config, authenticated, handle_request, Format
from config import *

app = typer.Typer(help="ntuaFLIX CLI manager")

@app.command()
def login(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        passw:      Annotated[str, typer.Option(help="Password", show_default=False)]
        ):
    store_config("api_key", None)
    try:
        response = requests.post(API_URL + "/login", params={'username': username, 'password': passw})

        if response.status_code == 200:
            response = response.json()
            if "token" in response:
                store_config("api_key", response.json()["token"])
                print(":white_check_mark: [bold green]You have been successfully authenticated.[/bold green]")
        elif response.status_code == 401:
            print(":stop_sign: [bold orange1]Unfortunately you were not authenticated (possibly due to wrong credentials). Please try again.[/bold orange1]")
        else:
            print(":no_good: [bold red]Server responded in an irregular manner (bad status code). Please contact system administrator.[/bold red]")
    except requests.JSONDecodeError:
        print(":no_good: [bold red]Server responded in an irregular manner (bad JSON). Please contact system administrator.[/bold red]")
    except requests.ConnectionError:
        print(":cross_mark: [bold bright_black]Server is down.[/bold bright_black]")

@app.command()
@authenticated
def logout():
    try:
        response = requests.post(API_URL + "/logout", headers={"X-OBSERVATORY-AUTH": api_key})
        if response.status_code == 200:
            print(":white_check_mark: [bold green]You have been successfully logged out")
        else:
            print(":no_good: [bold red]Server responded in an irregular manner (bad status code). Please contact system administrator.[/bold red]")
            print(":white_exclamation_mark: [bright_black]Although server probably failed, your authentication token has been deleted from local db.")
    except requests.ConnectionError:
        print(":cross_mark: [bright_black]Server is down.[/bright_black]")
        print(":white_exclamation_mark: [bright_black]Your authentication token will be deleted from local db, though the server will not become aware of this.") 
    store_config("api_key", None)

@app.command()
@authenticated
def adduser(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        passw:      Annotated[str, typer.Option(help="Password", show_default=False)] 
        ):
    response = handle_request(f"/admin/usermod/{urllib.parse.quote(username)}/{urllib.parse.quote(passw)}", api_key=api_key)
    if response is not None:
        print(":white_check_mark: [bold green]User successfully created.[/bold green]")

@app.command()
@authenticated
def user(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):

    response = handle_request(f"/admin/usermod/{urllib.parse.quote(username)}", api_key=api_key, parse_json=True if format==Format.json else False)
    if response is not None:
        if format == format.json:
            if response == {}:
                print(":magnifying_glass_tilted_right: [bold bright_black]User not found.[/bold bright_black]")
            else:
                print(":white_check_mark: [bold green]User found with with following details.[/bold green]")
                print_json(response)
        elif format == format.csv:
            print_csv(response.text)
            #TODO: what if no user?

if __name__ == '__main__':
    app()

