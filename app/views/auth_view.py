import click
from sqlalchemy.orm import sessionmaker
from app.init_db import engine
from app.controllers.auth_controller import authenticate_user, get_user_by_token
import configparser

# Initialize the session with the database
Session = sessionmaker(bind=engine)
session = Session()

# Define the configuration file to store authentication tokens
CONFIG_FILE = "auth_token.ini"
config = configparser.ConfigParser()


def save_token_to_ini(token):
    """
    Save the authentication token to an INI file.

    Args:
        token (str): The token to save.
    """

    config['AUTH'] = {'token': token}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def load_token_from_ini():
    """
    Load the authentication token from the INI file.

    Returns:
        str or None: The loaded token if available, None otherwise.
    """

    config.read(CONFIG_FILE)
    return config['AUTH']['token'] if 'AUTH' in config and 'token' in config['AUTH'] else None


def delete_token_from_ini():
    """
    Delete the authentication token from the INI file.
    """

    if 'AUTH' in config:
        config.remove_section('AUTH')
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)



# Load the current token from the configuration file to maintain login state across sessions
current_token = load_token_from_ini()


@click.group()
def auth_cli():
    pass



@auth_cli.command('login')
@click.option('--employee_number', prompt='Employee Number', help='Your employee number')
@click.option('--password', prompt='Password', hide_input=True, help='Your password')
def login(employee_number, password):
    """
    Authenticate the user and save the authentication token.

    Args:
        employee_number (str): The employee number for authentication.
        password (str): The user's password for authentication.

    The token is saved in an INI file upon successful authentication.
    """

    global current_token
    current_token = authenticate_user(session, employee_number, password)
    if current_token:
        save_token_to_ini(current_token)
        click.echo(f'Authenticated successfully! Your token: {current_token}')
    else:
        click.echo('Authentication failed')


@auth_cli.command('logout')
def logout():
    """
    Log out the current user by deleting the authentication token.
    """

    global current_token
    if current_token:
        click.echo('Logged out successfully!')
        delete_token_from_ini()
        current_token = None
    else:
        click.echo('No user is currently logged in')


@auth_cli.command('status')
def status():
    """
    Check the current login status.

    If a user is logged in, display their full name. Otherwise, indicate that no user is logged in.
    """

    global current_token
    if current_token:
        user = get_user_by_token(session, current_token)
        if user:
            click.echo(f'Logged in as: {user.full_name}')
        else:
            click.echo('Invalid token')
    else:
        click.echo('No user is currently logged in')


if __name__ == '__main__':
    auth_cli()
