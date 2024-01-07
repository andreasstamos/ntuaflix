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
    """Logs in and stores token to local storage."""
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
    """Logs out and deletes token from local storage."""
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
    """Adds user to system. Requires authentication."""
    response = handle_request(f"/admin/usermod/{urllib.parse.quote(username)}/{urllib.parse.quote(passw)}", api_key=api_key)
    if response is not None:
        print(":white_check_mark: [bold green]User successfully created.[/bold green]")
    else:
        print(":cross_mark: [bold red]User creation failed for unknownr reason.[/bold red]")


@app.command()
@authenticated
def user(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Returns user details. Requires authentication."""
    response = handle_request(f"/admin/usermod/{urllib.parse.quote(username)}", api_key=api_key)
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]User found with with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]User not found.[/bold bright_black]"
                )


@app.command()
@authenticated
def healthcheck(
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Checks the health of the API. Requires authentication."""
    response = handle_request("/admin/healthcheck")
    if response is not None:
        print_response(response, format=format)

@app.command()
def resetall(
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Resets database to initial state. Requires authentication."""
    response = handle_request("/admin/resetall")
    if response is not None:
        print_response(response, format=format)


@app.command()
def newtitles(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Titles. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/titlebasics", data=f)
    if response is not None:
        print_response(response, format=format)

@app.command()
def newakas(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Aliases. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/titleakas", data=f)
    if response is not None:
        print_response(response, format=format)

@app.command()
def newnames(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Aliases. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/namebasics", data=f)
    if response is not None:
        print_response(response, format=format)

@app.command()
def newcrew(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Crews. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/titlecrew", data=f)
    if response is not None:
        print_response(response, format=format)

@app.command()
def newepisode(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Episodes. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/titleepisode", data=f)
    if response is not None:
        print_response(response, format=format)

@app.command()
def newprincipals(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Title Principals. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/titleprincipals", data=f)
    if response is not None:
        print_response(response, format=format)

@app.command()
def newratings(
        filename: Annotated[Format, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Title Ratings. Requires authentication."""
    with open(filename, "rb") as f:
        response = handle_request("/admin/upload/titleratings", data=f)
    if response is not None:
        print_response(response, format=format)


if __name__ == '__main__':
    app()

