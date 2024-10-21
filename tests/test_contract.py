from unittest.mock import patch
from app.controllers.contract_controller import (create_contract, get_all_contracts, update_contract,
                                                 delete_contract, sign_contract, get_contract)
from app.models.user import User
from app.models.role import Role
from app.models.client import Client
from app.models.contract import Contract


def test_create_contract_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin001', full_name='Admin User', email='admin@example.com', role=role)
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

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=admin_user):
        create_contract(
            token='fake_token',
            session=session,
            client_id=client.id,
            sales_contact_id=admin_user.id,
            total_amount=5000,
            amount_due=1000,
            creation_date='2023-01-01',
            status='Pending'
        )


def test_create_contract_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=support_user):
        contract = create_contract('fake_token', session, client_id=1, sales_contact_id=2, total_amount=1000,
                                   amount_due=500, creation_date='2023-01-01', status='Pending')

        assert contract is None, "Contract should not have been created as the user lacks 'create_contract' permission"


def test_get_all_contracts_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()

    admin_user = User(employee_number='admin001', full_name='Admin User', email='admin@example.com', role=role)
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

    contract = Contract(
        client_id=client.id,
        sales_contact_id=admin_user.id,
        total_amount=5000,
        amount_due=1000,
        creation_date='2023-01-01',
        status='Pending'
    )
    session.add(contract)
    session.commit()

    contract_in_db = session.query(Contract).filter_by(id=contract.id).first()
    assert contract_in_db is not None, "Le contrat n'a pas été trouvé dans la base de données"

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=admin_user):
        contracts = get_all_contracts('fake_token', session)

        contract_ids = [c.id for c in contracts]
        assert contract.id in contract_ids, f"Le contrat {contract.id} devrait être dans la liste des contrats"


def test_get_all_contracts_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=support_user):
        contracts = get_all_contracts('fake_token', session)

        assert contracts is None, "Contracts should not be retrieved as the user lacks 'view_contract' permission"


def test_update_contract_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin003', full_name='Admin User', email='admin3@example.com', role=role)
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

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id,
                        total_amount=5000, amount_due=1000, creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=admin_user):
        update_contract(token='fake_token', session=session, contract_id=contract.id, status='Signed')

        updated_contract = session.query(Contract).filter_by(id=contract.id).first()
        assert updated_contract.status == 'Signed', "Le statut du contrat devrait être 'Signed'"


def test_update_contract_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=support_user):
        updated_contract = update_contract('fake_token', session, contract_id=1, status='Signed')

        assert updated_contract is None, ("Contract should not have been updated "
                                          "as the user lacks 'update_contract' permission")


def test_delete_contract_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin004', full_name='Admin User', email='admin4@example.com', role=role)
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

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000,
                        amount_due=1000, creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    initial_contract_count = session.query(Contract).count()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=admin_user):
        deleted_contract = delete_contract('fake_token', session, contract.id)

        assert deleted_contract is not None, "Contract should have been deleted"

    final_contract_count = session.query(Contract).count()

    assert final_contract_count == initial_contract_count - 1, "Contract count should have decreased by 1"


def test_delete_contract_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=support_user):
        deleted_contract = delete_contract('fake_token', session, contract_id=1)

        assert deleted_contract is None, ("Contract should not have been deleted "
                                          "as the user lacks 'delete_contract' permission")


def test_sign_contract(session):
    client = Client(
        full_name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date='2023-01-01',
        last_contact_date='2023-01-15',
        contact_person="John Doe"
    )
    session.add(client)
    session.commit()

    sales_contact = User(employee_number='sales001', full_name='Sales User', email='salesuser@example.com')
    role = session.query(Role).filter_by(role_name='Gestion').first()

    assert role is not None, "Role 'Gestion' not found"
    assert 'sign_contract' in role.permissions, "'sign_contract' not in Gestion role permissions"

    sales_contact.role = role
    session.add(sales_contact)
    session.commit()

    contract = Contract(
        client_id=client.id,
        sales_contact_id=sales_contact.id,
        total_amount=5000,
        amount_due=1000,
        creation_date='2023-01-01',
        status='Pending'
    )
    session.add(contract)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=sales_contact):
        signed_contract = sign_contract(token='fake_token', session=session, contract_id=contract.id)
        assert signed_contract.status == 'Signed', "Le statut du contrat devrait être 'Signed'"


def test_get_contract_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin005', full_name='Admin User', email='adminuser5@example.com', role=role)
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

    contract = Contract(client_id=client.id, sales_contact_id=admin_user.id, total_amount=5000,
                        amount_due=1000, creation_date='2023-01-01', status='Pending')
    session.add(contract)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=admin_user):
        retrieved_contract = get_contract('fake_token', session, contract.id)

        assert retrieved_contract is not None, "Contract should have been retrieved"
        assert retrieved_contract.total_amount == 5000, "Contract total amount should match"


def test_get_contract_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support005', full_name='Support User',
                        email='supportuser5@example.com', role=role)
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

    contract = Contract(
        client_id=client.id,
        sales_contact_id=support_user.id,
        total_amount=5000,
        amount_due=1000,
        creation_date='2023-01-01',
        status='Pending'
    )
    session.add(contract)
    session.commit()

    with patch('app.controllers.contract_controller.get_user_by_token', return_value=support_user):
        retrieved_contract = get_contract('fake_token', session, contract.id)

        assert retrieved_contract is None, ("Contract should not have been retrieved "
                                            "as the user lacks 'view_contract' permission")
