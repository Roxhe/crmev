import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.role import Role


DATABASE_TEST_URL = "postgresql://postgres:password@localhost/test_crmev"


engine_test = create_engine(DATABASE_TEST_URL)

SessionTest = sessionmaker(bind=engine_test)

def init_db_test():
    Base.metadata.drop_all(engine_test)
    Base.metadata.create_all(engine_test)
    add_default_roles()

def add_default_roles():
    roles = [
        Role(role_name='Commercial', permissions='create_client,view_client,update_client,delete_client,'
                                                 'view_contract,create_event'),
        Role(role_name='Support', permissions=''),
        Role(role_name='Gestion', permissions='create_user,view_user,update_user,delete_user,view_all,create_contract,'
                                              'view_contract,update_contract,sign_contract,delete_contract,'
                                              'create_event,view_event,update_event,delete_event,'
                                              'create_client,view_client,update_client,delete_client')
    ]
    session = SessionTest()
    session.add_all(roles)
    session.commit()
    session.close()


@pytest.fixture(scope='function', autouse=True)
def setup_test_db():
    init_db_test()
    yield
    init_db_test()


@pytest.fixture(scope='function')
def session():
    session_test = SessionTest()
    yield session_test
    session_test.close()
