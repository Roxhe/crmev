import click
from sqlalchemy.orm import sessionmaker
from app.init_db import engine
from app.controllers.event_controller import (create_event, get_event, get_all_events, update_event, delete_event, PermissionError)
from app.decorators import load_token

# Create a new database session
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def event_cli():
    pass

@event_cli.command('create-event')
@click.option('--contract_id', prompt='Contract ID', help='The ID of the contract associated with the event')
@click.option('--client_name', prompt='Client Name', help='The name of the client associated with the event')
@click.option('--client_contact', prompt='Client Contact', help='The contact information of the client')
@click.option('--start_date', prompt='Start Date', help='The start date and time of the event')
@click.option('--end_date', prompt='End Date', help='The end date and time of the event')
@click.option('--support_contact', prompt='Support Contact ID', help='The ID of the support contact responsible for the event')
@click.option('--location', prompt='Location', help='The location of the event')
@click.option('--attendees', prompt='Number of Attendees', type=int, help='The number of attendees expected at the event')
@click.option('--notes', prompt='Notes', help='Additional notes for the event')
@load_token
def create_event_cmd(user, contract_id, client_name, client_contact, start_date, end_date, support_contact, location, attendees, notes):
    """
    Create a new event.

    Args:
        user: The authenticated user making the request.
        contract_id (int): The ID of the contract associated with the event.
        client_name (str): The name of the client associated with the event.
        client_contact (str): The contact information of the client.
        start_date (str): The start date and time of the event.
        end_date (str): The end date and time of the event.
        support_contact (int): The ID of the support contact responsible for the event.
        location (str): The location of the event.
        attendees (int): The number of attendees expected at the event.
        notes (str): Additional notes for the event.
    """

    try:
        event = create_event(user, session, contract_id, client_name, client_contact, start_date, end_date, support_contact, location, attendees, notes)
        click.echo(f'Event for client {event.client_name} created successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@event_cli.command('get-event')
@click.option('--event_id', prompt='Event ID', help='The ID of the event to retrieve')
@load_token
def get_event_cmd(user, event_id):
    """
    Retrieve an event by its ID.

    Args:
        user: The authenticated user making the request.
        event_id (int): The ID of the event to retrieve.
    """

    try:
        event = get_event(user, session, event_id)
        if event:
            click.echo(f'Event ID: {event.id}, Client: {event.client_name}, Location: {event.location}, Start Date: {event.start_date}')
        else:
            click.echo('Event not found')
    except PermissionError as e:
        click.echo(str(e))

@event_cli.command('get-all-events')
@load_token
def get_all_events_cmd(user):
    """
    Retrieve all events.

    Args:
        user: The authenticated user making the request.
    """

    try:
        events = get_all_events(user, session)
        for event in events:
            click.echo(f'Event ID: {event.id}, Client: {event.client_name}, Location: {event.location}, Start Date: {event.start_date}')
    except PermissionError as e:
        click.echo(str(e))

@event_cli.command('update-event')
@click.option('--event_id', prompt='Event ID', help='The ID of the event to update')
@click.option('--client_name', prompt='Client Name', required=False, help='The new name of the client')
@click.option('--client_contact', prompt='Client Contact', required=False, help='The new contact information of the client')
@click.option('--start_date', prompt='Start Date', required=False, help='The new start date and time of the event')
@click.option('--end_date', prompt='End Date', required=False, help='The new end date and time of the event')
@click.option('--support_contact', prompt='Support Contact ID', required=False, help='The new support contact ID')
@click.option('--location', prompt='Location', required=False, help='The new location of the event')
@click.option('--attendees', prompt='Number of Attendees', type=int, required=False, help='The new number of attendees')
@click.option('--notes', prompt='Notes', required=False, help='The new notes for the event')
@load_token
def update_event_cmd(user, event_id, client_name, client_contact, start_date, end_date, support_contact, location, attendees, notes):
    """
    Update an existing event.

    Args:
        user: The authenticated user making the request.
        event_id (int): The ID of the event to update.
        client_name (str, optional): The new name of the client.
        client_contact (str, optional): The new contact information of the client.
        start_date (str, optional): The new start date and time of the event.
        end_date (str, optional): The new end date and time of the event.
        support_contact (int, optional): The new support contact ID.
        location (str, optional): The new location of the event.
        attendees (int, optional): The new number of attendees.
        notes (str, optional): The new notes for the event.
    """

    try:
        event = update_event(user, session, event_id, client_name, client_contact, start_date, end_date, support_contact, location, attendees, notes)
        click.echo(f'Event {event.id} updated successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

@event_cli.command('delete-event')
@click.option('--event_id', prompt='Event ID', help='The ID of the event to delete')
@load_token
def delete_event_cmd(user, event_id):
    """
    Delete an event by its ID.

    Args:
        user: The authenticated user making the request.
        event_id (int): The ID of the event to delete.
    """

    try:
        delete_event(user, session, event_id)
        click.echo('Event deleted successfully!')
    except (ValueError, PermissionError) as e:
        click.echo(str(e))

if __name__ == '__main__':
    event_cli()
