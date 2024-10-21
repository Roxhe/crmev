import click
import sentry_sdk
from views.user_view import user_cli
from views.client_view import client_cli
from views.contract_view import contract_cli
from views.event_view import event_cli
from views.auth_view import auth_cli

# Initialize Sentry SDK for error tracking and performance monitoring
sentry_sdk.init(
    dsn="https://9fc79b06412adb371b09205f9c21cad1@o4507974401589248.ingest.de.sentry.io/4507974419218512",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@click.group()
def cli():
    pass

# Add subcommands to the main command group
cli.add_command(user_cli, name='user')
cli.add_command(client_cli, name='client')
cli.add_command(contract_cli, name='contract')
cli.add_command(event_cli, name='event')
cli.add_command(auth_cli, name='auth')


if __name__ == '__main__': # Run the CLI application
    cli()
