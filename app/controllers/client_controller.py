from sqlalchemy.orm import Session
from app.models.client import Client
from app.controllers.auth_controller import get_user_by_token


class PermissionError(Exception):
    pass

"""CREATE"""
def create_client(token: str, session: Session, full_name, email, phone, company_name, creation_date,
                  last_contact_date, contact_person):
    """
    Create a new client in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        full_name (str): The full name of the client.
        email (str): The email address of the client.
        phone (str): The phone number of the client.
        company_name (str): The name of the client's company.
        creation_date (Date): The date when the client was created.
        last_contact_date (Date): The date when the client was last contacted.
        contact_person (str): The contact person for the client.

    Returns:
        Client or None: The created client object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('create_client'):
        return None

    try:
        new_client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            creation_date=creation_date,
            last_contact_date=last_contact_date,
            contact_person=contact_person
        )
        session.add(new_client)
        session.commit()
        session.refresh(new_client)
        return new_client

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création du client: {e}")
        return None

"""READ"""
def get_client(token: str, session: Session, client_id):
    """
    Retrieve a client from the database by their ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.
        client_id (int): The ID of the client to retrieve.

    Returns:
        Client or None: The client object if found and permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_client'):
        return None

    return session.query(Client).filter(Client.id == client_id).first()


def get_all_clients(token: str, session: Session):
    """
    Retrieve all clients from the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.

    Returns:
        list[Client] or None: A list of all client objects if permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_client'):
        return None

    return session.query(Client).all()

"""UPDATE"""
def update_client(token: str, session, client_id, full_name=None, email=None, phone=None, company_name=None,
                  last_contact_date=None, contact_person=None):
    """
    Update an existing client in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        client_id (int): The ID of the client to update.
        full_name (str, optional): The new full name of the client.
        email (str, optional): The new email address of the client.
        phone (str, optional): The new phone number of the client.
        company_name (str, optional): The new company name of the client.
        last_contact_date (Date, optional): The new last contact date of the client.
        contact_person (str, optional): The new contact person for the client.

    Returns:
        Client or None: The updated client object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('update_client'):
        return None

    client = session.query(Client).filter(Client.id == client_id).first()
    if client:
        if full_name:
            client.full_name = full_name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if company_name:
            client.company_name = company_name
        if last_contact_date:
            client.last_contact_date = last_contact_date
        if contact_person:
            client.contact_person = contact_person
        session.commit()

"""DELETE"""
def delete_client(token: str, session, client_id):
    """
    Delete a client from the database by their ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        client_id (int): The ID of the client to delete.

    Returns:
        Client or None: The deleted client object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('delete_client'):
        return None

    client = session.query(Client).filter(Client.id == client_id).first()
    if client:
        session.delete(client)
        session.commit()
        return client
    return None
