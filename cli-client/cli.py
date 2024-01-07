from typing import Annotated, Optional
import typer
from rich import print, print_json
import requests
import urllib
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
@authenticated
def resetall(
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Resets database to initial state. Requires authentication."""
    response = handle_request("/admin/resetall")
    if response is not None:
        print_response(response, format=format)


@app.command()
@authenticated
def newtitles(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Titles. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titlebasics", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def newakas(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Aliases. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleakas", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def newnames(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Aliases. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/namebasics", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def newcrew(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Crews. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titlecrew", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def newepisode(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Episodes. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleepisode", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def newprincipals(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Title Principals. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleprincipals", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def newratings(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Uploads data for Title Ratings. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleratings", data=f)
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def title(
        titleID: Annotated[str, typer.Option("--titleID", help="ID of title (tconst)")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Searches for title details based on title ID. Requires authentication."""
    response = handle_request(f"/title/{urllib.parse.quote(titleID)}")
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def searchtitle(
        titlepart: Annotated[str, typer.Option("--titleID", help="Substring of primary title.")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Searches for titles that their primary title contains a given string. Requires authentication."""
    response = handle_request(f"/searchtitle", method="GET", payload={"titlepart": titlepart})
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def bygenre(
        genre: Annotated[str, typer.Option(help="Genre")],
        _min: Annotated[int, typer.Option("--min", help="Minimum rating.")],
        _from: Annotated[Optional[int], typer.Option("--from", help="Start year must be after this year. If defined '--to' must also be defined.")] = None,
        to: Annotated[Optional[int], typer.Option(help="Start year must be before this year. If defined '--from' must also be defined.")] = None
        ):
    """Searches for titles using criteria. Requires authentication."""

    if (_from is None) != (to is None):
        print(":no_entry: [bold red]Options '--from', '--to' must either both be defined or neither.[/bold red]")
        return
    payload = {'qgenre': genre, 'minrating': _min}
    if _from is not None:
        payload["yrFrom"] = _from
        payload["yrTo"] = to
    response = handle_request(f"/bygenre", method="GET", payload=payload)
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def name(
        nameid: Annotated[str, typer.Option(help="ID of person (nconst)")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Searches for person details based on name ID. Requires authentication."""
    response = handle_request(f"/name/{urllib.parse.quote(nameid)}")
    if response is not None:
        print_response(response, format=format)

@app.command()
@authenticated
def searchname(
        namepart: Annotated[str, typer.Option("--titleID", help="Substring of name.")],
        format: Annotated[Format, typer.Option(help="Format to query")] = f"{Format.json}"
        ):
    """Searches for peoples that their name contains a given string. Requires authentication."""
    response = handle_request(f"/searchname", method="GET", payload={"namepart": namepart})
    if response is not None:
        print_response(response, format=format)


if __name__ == '__main__':
    app()

