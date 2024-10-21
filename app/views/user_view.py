import click
from sqlalchemy.orm import sessionmaker
from app.init_db import engine
from app.controllers.user_controller import (create_user, get_user, get_all_users, update_user, delete_user, PermissionError)
from app.decorators import load_token

# Create a new database session
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def user_cli():
    pass

@user_cli.command('create-user')
@click.option('--employee_number', prompt='Employee Number', help='The employee number of the user')
@click.option('--password', prompt='Password', hide_input=True, help='The password of the user')
@click.option('--email', prompt='Email', help='The email address of the user')
@click.option('--full_name', prompt='Full Name', help='The full name of the user')
@click.option('--department', prompt='Department', help='The department of the user')
@click.option('--role_name', prompt='Role Name', help='The role name to assign to the user')
@load_token
def create_user_cmd(user, employee_number, password, email, full_name, department, role_name):
    """
    Create a new user.

    Args:
        user: The authenticated user making the request.
        employee_number (str): The employee number of the user.
        password (str): The password of the user.
        email (str): The email address of the user.
        full_name (str): The full name of the user.
        department (str): The department of the user.
        role_name (str): The role name to assign to the user.
    """

    try:
        new_user = create_user(user, session, employee_number, password, email, full_name, department, role_name)
        click.echo(f'User {new_user.full_name} created successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@user_cli.command('get-user')
@click.option('--user_id', prompt='User ID', help='The ID of the user to retrieve')
@load_token
def get_user_cmd(user, user_id):
    """
    Retrieve a user by their ID.

    Args:
        user: The authenticated user making the request.
        user_id (int): The ID of the user to retrieve.
    """

    try:
        retrieved_user = get_user(user, session, user_id)
        if retrieved_user:
            click.echo(f'User: {retrieved_user.full_name}, Email: {retrieved_user.email}, Department: {retrieved_user.department}')
        else:
            click.echo('User not found')
    except PermissionError as e:
        click.echo(str(e))

@user_cli.command('get-all-users')
@load_token
def get_all_users_cmd(user):
    """
    Retrieve all users.

    Args:
        user: The authenticated user making the request.
    """

    try:
        users = get_all_users(user, session)
        for user in users:
            click.echo(f'User: {user.full_name}, Email: {user.email}, Department: {user.department}')
    except PermissionError as e:
        click.echo(str(e))

@user_cli.command('update-user')
@click.option('--user_id', prompt='User ID', help='The ID of the user to update')
@click.option('--employee_number', prompt='Employee Number', required=False, help='The new employee number of the user')
@click.option('--password', prompt='Password', hide_input=True, required=False, help='The new password of the user')
@click.option('--email', prompt='Email', required=False, help='The new email address of the user')
@click.option('--full_name', prompt='Full Name', required=False, help='The new full name of the user')
@click.option('--department', prompt='Department', required=False, help='The new department of the user')
@click.option('--role_name', prompt='Role Name', required=False, help='The new role name to assign to the user')
@load_token
def update_user_cmd(user, user_id, employee_number, password, email, full_name, department, role_name):
    """
    Update an existing user.

    Args:
        user: The authenticated user making the request.
        user_id (int): The ID of the user to update.
        employee_number (str, optional): The new employee number of the user.
        password (str, optional): The new password of the user.
        email (str, optional): The new email address of the user.
        full_name (str, optional): The new full name of the user.
        department (str, optional): The new department of the user.
        role_name (str, optional): The new role name to assign to the user.
    """

    try:
        updated_user = update_user(user, session, user_id, employee_number, password, email, full_name, department, role_name)
        click.echo(f'User {updated_user.full_name} updated successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@user_cli.command('delete-user')
@click.option('--user_id', prompt='User ID', help='The ID of the user to delete')
@load_token
def delete_user_cmd(user, user_id):
    """
    Delete a user by their ID.

    Args:
        user: The authenticated user making the request.
        user_id (int): The ID of the user to delete.
    """

    try:
        delete_user(user, session, user_id)
        click.echo('User deleted successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

if __name__ == '__main__':
    user_cli()
