import click
from sqlalchemy.orm import sessionmaker
from app.init_db import engine
from app.controllers.client_controller import (create_client, get_client, get_all_clients, update_client,
                                               delete_client, PermissionError)
from app.decorators import load_token

# Create a new database session
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def client_cli():
    pass

@client_cli.command('create-client')
@click.option('--name', prompt='Client Name', help='The name of the client')
@click.option('--email', prompt='Email', help='The email of the client')
@load_token
def create_client_cmd(user, name, email):
    """
    Create a new client.

    Args:
        user: The authenticated user making the request.
        name (str): The name of the client.
        email (str): The email of the client.
    """

    try:
        client = create_client(user, session, name, email)
        click.echo(f'Client {client.name} created successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@client_cli.command('get-client')
@click.option('--client_id', prompt='Client ID', help='The ID of the client to retrieve')
@load_token
def get_client_cmd(user, client_id):
    """
    Retrieve a client by their ID.

    Args:
        user: The authenticated user making the request.
        client_id (int): The ID of the client to retrieve.
    """

    try:
        client = get_client(user, session, client_id)
        if client:
            click.echo(f'Client: {client.name}, Email: {client.email}')
        else:
            click.echo('Client not found')
    except PermissionError as e:
        click.echo(str(e))

@client_cli.command('get-all-clients')
@load_token
def get_all_clients_cmd(user):
    """
    Retrieve all clients.

    Args:
        user: The authenticated user making the request.
    """

    try:
        clients = get_all_clients(user, session)
        for client in clients:
            click.echo(f'Client: {client.name}, Email: {client.email}')
    except PermissionError as e:
        click.echo(str(e))

@client_cli.command('update-client')
@click.option('--client_id', prompt='Client ID', help='The ID of the client to update')
@click.option('--name', prompt='Client Name', help='The name of the client', required=False)
@click.option('--email', prompt='Email', help='The email of the client', required=False)
@load_token
def update_client_cmd(user, client_id, name, email):
    """
    Update an existing client.

    Args:
        user: The authenticated user making the request.
        client_id (int): The ID of the client to update.
        name (str, optional): The new name of the client.
        email (str, optional): The new email of the client.
    """

    try:
        client = update_client(user, session, client_id, name, email)
        click.echo(f'Client {client.name} updated successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@client_cli.command('delete-client')
@click.option('--client_id', prompt='Client ID', help='The ID of the client to delete')
@load_token
def delete_client_cmd(user, client_id):
    """
    Delete a client by their ID.

    Args:
        user: The authenticated user making the request.
        client_id (int): The ID of the client to delete.
    """

    try:
        delete_client(user, session, client_id)
        click.echo('Client deleted successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

if __name__ == '__main__':
    client_cli()
