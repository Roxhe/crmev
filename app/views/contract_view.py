import click
from sqlalchemy.orm import sessionmaker
from app.init_db import engine
from app.controllers.contract_controller import (create_contract, get_contract, get_all_contracts, update_contract,
                                                 delete_contract, sign_contract, PermissionError)
from app.decorators import load_token

# Create a new database session
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def contract_cli():
    pass

@contract_cli.command('create-contract')
@click.option('--client_id', prompt='Client ID', help='The ID of the client associated with the contract')
@click.option('--sales_contact_id', prompt='Sales Contact ID', help='The ID of the sales contact responsible for the contract')
@click.option('--total_amount', prompt='Total Amount', type=float, help='The total amount of the contract')
@click.option('--amount_due', prompt='Amount Due', type=float, help='The amount due for the contract')
@click.option('--creation_date', prompt='Creation Date', help='The creation date of the contract')
@click.option('--status', prompt='Status', help='The status of the contract')
@load_token
def create_contract_cmd(user, client_id, sales_contact_id, total_amount, amount_due, creation_date, status):
    """
    Create a new contract.

    Args:
        user: The authenticated user making the request.
        client_id (int): The ID of the client associated with the contract.
        sales_contact_id (int): The ID of the sales contact responsible for the contract.
        total_amount (float): The total amount of the contract.
        amount_due (float): The amount due for the contract.
        creation_date (str): The creation date of the contract.
        status (str): The status of the contract.
    """

    try:
        contract = create_contract(user, session, client_id, sales_contact_id, total_amount, amount_due, creation_date, status)
        click.echo(f'Contract for client {contract.client_id} created successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@contract_cli.command('get-contract')
@click.option('--contract_id', prompt='Contract ID', help='The ID of the contract to retrieve')
@load_token
def get_contract_cmd(user, contract_id):
    """
    Retrieve a contract by its ID.

    Args:
        user: The authenticated user making the request.
        contract_id (int): The ID of the contract to retrieve.
    """

    try:
        contract = get_contract(user, session, contract_id)
        if contract:
            click.echo(f'Contract ID: {contract.id}, Total Amount: {contract.total_amount}, Status: {contract.status}')
        else:
            click.echo('Contract not found')
    except PermissionError as e:
        click.echo(str(e))

@contract_cli.command('get-all-contracts')
@load_token
def get_all_contracts_cmd(user):
    """
    Retrieve all contracts.

    Args:
        user: The authenticated user making the request.
    """

    try:
        contracts = get_all_contracts(user, session)
        for contract in contracts:
            click.echo(f'Contract ID: {contract.id}, Total Amount: {contract.total_amount}, Status: {contract.status}')
    except PermissionError as e:
        click.echo(str(e))

@contract_cli.command('update-contract')
@click.option('--contract_id', prompt='Contract ID', help='The ID of the contract to update')
@click.option('--sales_contact_id', prompt='Sales Contact ID', required=False, help='The new sales contact ID')
@click.option('--total_amount', prompt='Total Amount', type=float, required=False, help='The new total amount')
@click.option('--amount_due', prompt='Amount Due', type=float, required=False, help='The new amount due')
@click.option('--status', prompt='Status', required=False, help='The new status of the contract')
@load_token
def update_contract_cmd(user, contract_id, sales_contact_id, total_amount, amount_due, status):
    """
    Update an existing contract.

    Args:
        user: The authenticated user making the request.
        contract_id (int): The ID of the contract to update.
        sales_contact_id (int, optional): The new sales contact ID for the contract.
        total_amount (float, optional): The new total amount of the contract.
        amount_due (float, optional): The new amount due for the contract.
        status (str, optional): The new status of the contract.
    """

    try:
        contract = update_contract(user, session, contract_id, sales_contact_id, total_amount, amount_due, status)
        click.echo(f'Contract {contract.id} updated successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@contract_cli.command('delete-contract')
@click.option('--contract_id', prompt='Contract ID', help='The ID of the contract to delete')
@load_token
def delete_contract_cmd(user, contract_id):
    """
    Delete a contract by its ID.

    Args:
        user: The authenticated user making the request.
        contract_id (int): The ID of the contract to delete.
    """

    try:
        delete_contract(user, session, contract_id)
        click.echo('Contract deleted successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@contract_cli.command('sign-contract')
@click.option('--contract_id', prompt='Contract ID', help='The ID of the contract to sign')
@load_token
def sign_contract_cmd(user, contract_id):
    """
    Sign a contract by updating its status to 'Signed'.

    Args:
        user: The authenticated user making the request.
        contract_id (int): The ID of the contract to sign.
    """

    try:
        contract = sign_contract(user, session, contract_id)
        click.echo(f'Contract {contract.id} signed successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

if __name__ == '__main__':
    contract_cli()
