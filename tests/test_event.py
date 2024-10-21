from unittest.mock import patch
from app.controllers.event_controller import create_event, get_event, update_event, delete_event, get_all_events
from app.models.user import User
from app.models.client import Client
from app.models.event import Event
from app.models.role import Role
from app.models.contract import Contract

def test_create_event_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin007', full_name='Admin User', email='adminuser7@example.com', role=role)
    session.add(admin_user)
    session.commit()

    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=admin_user):
        new_event = create_event(
            token='fake_token',
            session=session,
            contract_id=contract.id,
            client_name="Test Client",
            client_contact="client_contact@example.com",
            start_date='2023-01-01',
            end_date='2023-01-05',
            support_contact=support_user,
            location="Office",
            attendees=10,
            notes="Test Event"
        )

        assert new_event is not None, "Event should have been created"

def test_create_event_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support002', full_name='Support User',
                        email='supportuser2@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=support_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=support_user):
        new_event = create_event(
            token='fake_token',
            session=session,
            contract_id=contract.id,
            client_name="Test Client",
            client_contact="client_contact@example.com",
            start_date='2023-01-01',
            end_date='2023-01-05',
            support_contact=support_user,
            location="Office",
            attendees=10,
            notes="Test Event"
        )

        assert new_event is None, "Event should not have been created as the user lacks 'create_event' permission"

def test_get_event_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin008', full_name='Admin User', email='adminuser8@example.com', role=role)
    session.add(admin_user)
    session.commit()

    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    event = Event(
        contract_id=contract.id,
        client_name="Test Client",
        client_contact="client_contact@example.com",
        start_date='2023-01-01',
        end_date='2023-01-05',
        support_contact=support_user,
        location="Office",
        attendees=10,
        notes="Test Event"
    )
    session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=admin_user):
        retrieved_event = get_event(token='fake_token', session=session, event_id=event.id)

        assert retrieved_event is not None, "Event should have been retrieved"

def test_get_event_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support003', full_name='Support User',
                        email='supportuser3@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=support_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    event = Event(
        contract_id=contract.id,
        client_name="Test Client",
        client_contact="client_contact@example.com",
        start_date='2023-01-01',
        end_date='2023-01-05',
        support_contact=support_user,
        location="Office",
        attendees=10,
        notes="Test Event"
    )
    session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=support_user):
        retrieved_event = get_event(token='fake_token', session=session, event_id=event.id)

        assert retrieved_event is None, "Event should not have been retrieved as the user lacks 'view_event' permission"

def test_update_event_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin009', full_name='Admin User', email='adminuser9@example.com', role=role)
    session.add(admin_user)
    session.commit()

    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    event = Event(
        contract_id=contract.id,
        client_name="Test Client",
        client_contact="client_contact@example.com",
        start_date='2023-01-01',
        end_date='2023-01-05',
        support_contact=support_user,
        location="Office",
        attendees=10,
        notes="Test Event"
    )
    session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=admin_user):
        updated_event = update_event(
            token='fake_token',
            session=session,
            event_id=event.id,
            client_name="Updated Client"
        )

        assert updated_event is not None, "Event should have been updated"
        assert updated_event.client_name == "Updated Client", "Event's client name should have been updated"

def test_update_event_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support004', full_name='Support User',
                        email='supportuser4@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=support_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    event = Event(
        contract_id=contract.id,
        client_name="Test Client",
        client_contact="client_contact@example.com",
        start_date='2023-01-01',
        end_date='2023-01-05',
        support_contact=support_user,
        location="Office",
        attendees=10,
        notes="Test Event"
    )
    session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=support_user):
        updated_event = update_event(
            token='fake_token',
            session=session,
            event_id=event.id,
            client_name="Updated Client"
        )

        assert updated_event is None, "Event should not have been updated as the user lacks 'update_event' permission"

def test_delete_event_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin010', full_name='Admin User', email='adminuser10@example.com', role=role)
    session.add(admin_user)
    session.commit()

    support_user = User(employee_number='support005', full_name='Support User',
                        email='supportuser5@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    event = Event(
        contract_id=contract.id,
        client_name="Test Client",
        client_contact="client_contact@example.com",
        start_date='2023-01-01',
        end_date='2023-01-05',
        support_contact=support_user,
        location="Office",
        attendees=10,
        notes="Test Event"
    )
    session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=admin_user):
        deleted_event = delete_event('fake_token', session, event.id)

        assert deleted_event is not None, "Event should have been deleted"

        remaining_event = session.query(Event).filter_by(id=event.id).first()
        assert remaining_event is None, "Event should no longer exist in the database"

def test_delete_event_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support006', full_name='Support User',
                        email='supportuser6@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=support_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    event = Event(
        contract_id=contract.id,
        client_name="Test Client",
        client_contact="client_contact@example.com",
        start_date='2023-01-01',
        end_date='2023-01-05',
        support_contact=support_user,
        location="Office",
        attendees=10,
        notes="Test Event"
    )
    session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=support_user):
        deleted_event = delete_event('fake_token', session, event.id)

        assert deleted_event is None, "Event should not have been deleted as the user lacks 'delete_event' permission"

        remaining_event = session.query(Event).filter_by(id=event.id).first()
        assert remaining_event is not None, "Event should still exist in the database"

def test_get_all_events_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin011', full_name='Admin User', email='adminuser11@example.com', role=role)
    session.add(admin_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    for i in range(3):
        event = Event(
            contract_id=contract.id,
            client_name=f"Test Client {i}",
            client_contact="client_contact@example.com",
            start_date='2023-01-01',
            end_date='2023-01-05',
            support_contact=admin_user,
            location="Office",
            attendees=10 + i,
            notes="Test Event"
        )
        session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=admin_user):
        events = get_all_events(token='fake_token', session=session)

        assert events is not None, "Events should have been retrieved"
        assert len(events) == 3, "There should be 3 events retrieved"


def test_get_all_events_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support007', full_name='Support User',
                        email='supportuser7@example.com', role=role)
    session.add(support_user)
    session.commit()

    client = Client(full_name="Test Client", email="client@example.com", phone="1234567890", company_name="Company",
                    contact_person="John Doe", creation_date='2023-01-01', last_contact_date='2023-01-15')
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, sales_contact_id=support_user.id, total_amount=5000, amount_due=1000,
                        creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    for i in range(3):
        event = Event(
            contract_id=contract.id,
            client_name=f"Test Client {i}",
            client_contact="client_contact@example.com",
            start_date='2023-01-01',
            end_date='2023-01-05',
            support_contact=support_user,
            location="Office",
            attendees=10 + i,
            notes="Test Event"
        )
        session.add(event)
    session.commit()

    with patch('app.controllers.event_controller.get_user_by_token', return_value=support_user):
        events = get_event(token='fake_token', session=session, event_id=None)

        assert events is None, "Events should not be retrieved as the user lacks 'view_event' permission"
