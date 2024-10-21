from unittest.mock import patch
from app.controllers.client_controller import create_client, get_client, get_all_clients, update_client, delete_client
from app.models.user import User
from app.models.role import Role
from app.models.client import Client


def test_create_client_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin001', full_name='Admin User', email='admin@example.com', role=role)
    session.add(admin_user)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=admin_user):
        created_client = create_client(
            token='fake_token',
            session=session,
            full_name="Test Client",
            email="client@example.com",
            phone="1234567890",
            company_name="Test Company",
            creation_date='2023-01-01',
            last_contact_date='2023-01-15',
            contact_person="John Doe"
        )

        assert created_client is not None, "Client should have been created"
        assert created_client.email == "client@example.com", "Created client's email should match"

        retrieved_client = session.query(Client).filter_by(email="client@example.com").first()
        assert retrieved_client is not None, "Client should exist in the database"
        assert retrieved_client.full_name == "Test Client", "Client's full name should match"



def test_create_client_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=support_user):
        created_client = create_client(
            token='fake_token',
            session=session,
            full_name="Test Client",
            email="client@example.com",
            phone="1234567890",
            company_name="Test Company",
            creation_date='2023-01-01',
            last_contact_date='2023-01-15',
            contact_person="John Doe"
        )

        assert created_client is None, ("Client should not have been created "
                                        "as the user lacks 'create_client' permission")


def test_get_client_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin002', full_name='Admin User', email='adminuser2@example.com', role=role)
    session.add(admin_user)
    session.commit()

    client = Client(
        full_name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=admin_user):
        retrieved_client = get_client('fake_token', session, client.id)
        assert retrieved_client is not None, "Client should have been retrieved"
        assert retrieved_client.full_name == "Test Client", "Client's name should match"


def test_get_client_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support002', full_name='Support User',
                        email='supportuser2@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(
        full_name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=support_user):
        retrieved_client = get_client('fake_token', session, client.id)
        assert retrieved_client is None, ("Client should not have been retrieved "
                                          "as the user lacks 'view_client' permission")


def test_get_all_clients_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin003', full_name='Admin User', email='adminuser3@example.com', role=role)
    session.add(admin_user)
    session.commit()

    client = Client(
        full_name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=admin_user):
        clients = get_all_clients('fake_token', session)
        assert len(clients) > 0, "Clients should have been retrieved"


def test_get_all_clients_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support003', full_name='Support User',
                        email='supportuser3@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=support_user):
        clients = get_all_clients('fake_token', session)
        assert clients is None, "Clients should not have been retrieved as the user lacks 'view_client' permission"


def test_update_client_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin004', full_name='Admin User', email='adminuser4@example.com', role=role)
    session.add(admin_user)
    session.commit()

    client = Client(
        full_name="Old Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=admin_user):
        update_client(
            token='fake_token',
            session=session,
            client_id=client.id,
            full_name="Updated Client"
        )

        updated_client = session.query(Client).filter_by(email="client@example.com").first()
        assert updated_client is not None, "Client should exist"
        assert updated_client.full_name == "Updated Client", "Client's name should have been updated"


def test_update_client_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support004', full_name='Support User',
                        email='supportuser4@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(
        full_name="Old Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=support_user):
        updated_client = update_client(
            token='fake_token',
            session=session,
            client_id=client.id,
            full_name="Unauthorized Update"
        )

        assert updated_client is None, ("Client should not have been updated as "
                                        "the user lacks 'update_client' permission")


def test_delete_client_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin005', full_name='Admin User', email='adminuser5@example.com', role=role)
    session.add(admin_user)
    session.commit()

    client = Client(
        full_name="Client To Delete",
        email="clienttodelete@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    initial_client_count = session.query(Client).count()

    with patch('app.controllers.client_controller.get_user_by_token', return_value=admin_user):
        deleted_client = delete_client('fake_token', session, client.id)

        assert deleted_client is not None, "Client should have been deleted"

    client_in_db = session.query(Client).filter_by(id=client.id).first()
    assert client_in_db is None, "Client should no longer exist in the database"

    final_client_count = session.query(Client).count()
    assert final_client_count == initial_client_count - 1, "Client count should have decreased by 1"


def test_delete_client_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support005', full_name='Support User',
                        email='supportuser5@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(
        full_name="Client To Delete",
        email="clienttodelete@example.com",
        phone="1234567890",
        company_name="Test Company",
        contact_person="John Doe",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15'
    )
    session.add(client)
    session.commit()

    with (patch('app.controllers.client_controller.get_user_by_token', return_value=support_user)):
        deleted_client = delete_client('fake_token', session, client.id)

        assert deleted_client is None, ("Client should not have been deleted "
                                        "as the user lacks 'delete_client' permission")

        remaining_client = session.query(Client).filter_by(id=client.id).first()
        assert remaining_client is not None, "Client should still exist in the database"
