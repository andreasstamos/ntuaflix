from typer.testing import CliRunner
import pytest
import os
from cli import app

from .utils import stdout_to_json

runner = CliRunner(mix_stderr=False)

def test_admin_login(login):
    pass

def test_health_check(login):
    result = runner.invoke(app, ["healthcheck"])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr

    result_json = stdout_to_json(result.stdout)

    assert result_json["status"] == "OK", result_json
    assert "dataconnection" in result_json, result_json
    assert isinstance(result_json["dataconnection"], str), result_json

