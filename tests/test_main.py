import pytest
from click.testing import CliRunner
from app.main import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])

    assert result.exit_code == 0, "CLI help command should execute successfully"
    assert 'Usage:' in result.output, "CLI help should include usage instructions"
    assert 'Commands:' in result.output, "CLI help should include list of commands"


@pytest.mark.parametrize("command", [
    "user",
    "client",
    "contract",
    "event",
    "auth"
])
def test_cli_commands(command):
    runner = CliRunner()
    result = runner.invoke(cli, [command, '--help'])

    assert result.exit_code == 0, f"CLI command '{command}' should execute successfully"
    assert 'Usage:' in result.output, f"'{command}' command help should include usage instructions"


def test_sentry_initialization():
    import sentry_sdk
    assert sentry_sdk.Hub.current.client is not None, "Sentry SDK should be initialized"
    assert (sentry_sdk.Hub.current.client.dsn ==
            "https://9fc79b06412adb371b09205f9c21cad1@o4507974401589248.ingest.de.sentry.io/4507974419218512"), \
        "Sentry DSN should match the expected value"
