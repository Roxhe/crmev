from sqlalchemy.orm import Session
from ..models.event import Event
from ..models.user import User
from ..controllers.auth_controller import get_user_by_token


class PermissionError(Exception):
    pass

def get_logged_in_user(session: Session, token: str) -> User:
    """
    Retrieve the logged-in user from the database using a JWT token.

    Args:
        session (Session): The database session to use for querying.
        token (str): The JWT token to verify.

    Returns:
        User or None: The user associated with the token if valid, None otherwise.
    """

    return get_user_by_token(session, token)

"""CREATE"""
def create_event(token: str, session: Session, contract_id, client_name, client_contact, start_date,
                 end_date, support_contact,location, attendees, notes):
    """
    Create a new event in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        contract_id (int): The ID of the contract associated with the event.
        client_name (str): The name of the client associated with the event.
        client_contact (str): The contact information of the client.
        start_date (DateTime): The start date and time of the event.
        end_date (DateTime): The end date and time of the event.
        support_contact (int): The ID of the support contact responsible for the event.
        location (str): The location of the event.
        attendees (int): The number of attendees expected at the event.
        notes (str): Additional notes for the event.

    Returns:
        Event or None: The created event object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('create_event'):
        return None

    new_event = Event(
        contract_id=contract_id,
        client_name=client_name,
        client_contact=client_contact,
        start_date=start_date,
        end_date=end_date,
        support_contact=support_contact,
        location=location,
        attendees=attendees,
        notes=notes
    )
    session.add(new_event)
    session.commit()
    return new_event

"""READ"""
def get_event(token: str, session, event_id):
    """
    Retrieve an event from the database by its ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.
        event_id (int): The ID of the event to retrieve.

    Returns:
        Event or None: The event object if found and permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_event'):
        return None

    return session.query(Event).filter(Event.id == event_id).first()


def get_all_events(token: str, session: Session, no_support=False, support_contact=None):
    """
    Retrieve all events from the database, with optional filters.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.
        no_support (bool, optional): If True, only retrieve events without a support contact assigned.
        support_contact (int, optional): The ID of the support contact to filter events by.

    Returns:
        list[Event] or None: A list of event objects if permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_event'):
        return None

    query = session.query(Event)

    if no_support:
        query = query.filter(Event.support_contact.is_(None))
    if support_contact:
        query = query.filter(Event.support_contact == support_contact)

    return query.all()

"""UPDATE"""
def update_event(token: str, session: Session, event_id, client_name=None, client_contact=None,
                 start_date=None, end_date=None,support_contact=None, location=None, attendees=None, notes=None):
    """
    Update an existing event in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        event_id (int): The ID of the event to update.
        client_name (str, optional): The new name of the client for the event.
        client_contact (str, optional): The new contact information of the client.
        start_date (DateTime, optional): The new start date and time of the event.
        end_date (DateTime, optional): The new end date and time of the event.
        support_contact (int, optional): The new support contact ID for the event.
        location (str, optional): The new location of the event.
        attendees (int, optional): The new number of attendees for the event.
        notes (str, optional): The new notes for the event.

    Returns:
        Event or None: The updated event object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('update_event'):
        return None

    event = session.query(Event).filter(Event.id == event_id).first()
    if event:
        if client_name:
            event.client_name = client_name
        if client_contact:
            event.client_contact = client_contact
        if start_date:
            event.start_date = start_date
        if end_date:
            event.end_date = end_date
        if support_contact:
            event.support_contact = support_contact
        if location:
            event.location = location
        if attendees:
            event.attendees = attendees
        if notes:
            event.notes = notes
        session.commit()
        return event

    return None

"""DELETE"""
def delete_event(token: str, session: Session, event_id):
    """
    Delete an event from the database by its ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        event_id (int): The ID of the event to delete.

    Returns:
        Event or None: The deleted event object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('delete_event'):
        return None

    event = session.query(Event).filter(Event.id == event_id).first()
    if event:
        session.delete(event)
        session.commit()
        return event

    return None
