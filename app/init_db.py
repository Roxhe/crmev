from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.role import Role
from models.user import User
from models.event import Event
from models.contract import Contract
from models.client import Client

# Define the database URL for connecting to PostgreSQL
DATABASE_URL = "postgresql://postgres:password@localhost/crmev?client_encoding=utf8"

# Create an engine that connects to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a session factory that binds to the engine
Session = sessionmaker(bind=engine)

# Instantiate a session to interact with the database
session = Session()

def init_db():
    """
    Initialize the database by creating all defined tables.
    """
    Base.metadata.create_all(engine)

def add_roles():
    """
    Add predefined roles to the database.

    The roles include:
    - 'Commercial': Has permissions for managing clients and viewing contracts.
    - 'Support': Has permissions for viewing and updating events.
    - 'Gestion': Has permissions for managing users, contracts, and events.
    """
    roles = [
        Role(role_name='Commercial', permissions='create_client,view_client,update_client,delete_client,'
                                                 'view_contract,create_event'),
        Role(role_name='Support', permissions='view_event,update_event'),
        Role(role_name='Gestion', permissions='create_user,update_user,delete_user,view_all,create_contract,'
                                              'view_contract,update_contract,sign_contract,delete_contract,'
                                              'view_event,update_event')
    ]
    session.add_all(roles)
    session.commit()

if __name__ == '__main__':
    init_db()
    add_roles()
