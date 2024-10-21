from app.controllers.user_controller import create_user, delete_user, update_user, get_user, get_all_users
from app.models.user import User
from app.models.role import Role


from unittest.mock import patch


def test_create_user_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()

    admin_user = User(employee_number='admin001', full_name='Admin User', email='admin@example.com', role=role)
    session.add(admin_user)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=admin_user):
        new_user = create_user(
            token='fake_token',
            session=session,
            employee_number='user001',
            password='password',
            email='user001@example.com',
            full_name='New User',
            department='HR',
            role_name='Support'
        )

        created_user = session.query(User).filter_by(email="user001@example.com").first()
        assert created_user is not None, "User should have been created"
        assert created_user.full_name == "New User", "User's full name should match"


def test_create_user_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support001', full_name='Support User', email='support@example.com', role=role)
    session.add(support_user)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=support_user):
        created_user = create_user('fake_token', session, 'user002', 'password',
                                   'user002@example.com', 'User No Permission',
                                   'HR', 'Support')

        assert created_user is None, "User should not have been created as support_user lacks 'create_user' permission"


def test_update_user_with_permissions(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()

    admin_user = User(employee_number='admin002', full_name='Admin User', email='adminuser2@example.com', role=role)
    session.add(admin_user)
    session.commit()

    user_to_update = User(
        employee_number="user002",
        full_name="Old User",
        email="olduser@example.com"
    )
    session.add(user_to_update)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=admin_user):
        update_user('fake_token', session, user_to_update.id, full_name="Updated User")

        updated_user = session.query(User).filter_by(email="olduser@example.com").first()
        assert updated_user is not None, "User should exist"
        assert updated_user.full_name == "Updated User", "User's name should have been updated"


def test_update_user_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support002', full_name='Support User',
                        email='supportuser2@example.com', role=role)
    session.add(support_user)
    session.commit()

    user_to_update = User(employee_number="user003", full_name="Old User", email="olduser@example.com")
    session.add(user_to_update)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=support_user):
        updated_user = update_user('fake_token', session, user_to_update.id, full_name="Unauthorized Update")

        assert updated_user is None, "User should not have been updated as support_user lacks 'update_user' permission"


def test_delete_user_with_permissions(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()

    admin_user = User(employee_number='admin003', full_name='Admin User', email='adminuser3@example.com', role=role)
    session.add(admin_user)
    session.commit()

    user_to_delete = User(employee_number="user004", full_name="User To Delete", email="usertodelete@example.com")
    session.add(user_to_delete)
    session.commit()

    initial_user_count = session.query(User).count()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=admin_user):
        deleted_user = delete_user('fake_token', session, user_to_delete.id)

        assert deleted_user is not None, "User should have been deleted"

    final_user_count = session.query(User).count()

    assert final_user_count == initial_user_count - 1, "User count should have decreased by 1"


def test_delete_user_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()

    support_user = User(employee_number='support003', full_name='Support User',
                        email='supportuser3@example.com', role=role)
    session.add(support_user)
    session.commit()

    user_to_delete = User(
        employee_number="user005",
        full_name="User To Delete",
        email="usertodelete2@example.com"
    )
    session.add(user_to_delete)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=support_user):
        deleted_user = delete_user('fake_token', session, user_to_delete.id)

        assert deleted_user is None, "User should not have been deleted as support_user lacks 'delete_user' permission"

        remaining_user = session.query(User).filter_by(id=user_to_delete.id).first()
        assert remaining_user is not None, "User should still exist in the database"


def test_get_all_users_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin005', full_name='Admin User', email='adminuser5@example.com', role=role)
    session.add(admin_user)
    session.commit()

    user_to_get = User(employee_number="user006", full_name="User to Get", email="usertoget@example.com")
    session.add(user_to_get)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=admin_user):
        users = get_all_users(admin_user, session)
        assert len(users) > 0, "Users should be retrieved"
        assert user_to_get.id in [user.id for user in users], "User should be in the retrieved list"


def test_get_user_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    admin_user = User(employee_number='admin004', full_name='Admin User', email='adminuser4@example.com', role=role)
    session.add(admin_user)
    session.commit()

    user_to_get = User(employee_number="user005", full_name="User to Get", email="usertoget@example.com")
    session.add(user_to_get)
    session.commit()

    with patch('app.controllers.user_controller.get_user_by_token', return_value=admin_user):
        retrieved_user = get_user('fake_token', session, user_to_get.id)

        print(f"User to get: {retrieved_user}")

        assert retrieved_user is not None, "User should have been retrieved"
        assert retrieved_user.full_name == "User to Get", "Retrieved user's name should match"


def test_get_user_no_permission(session):
    role = session.query(Role).filter_by(role_name='Support').first()
    support_user = User(employee_number='support004', full_name='Support User',
                        email='supportuser4@example.com', role=role)
    session.add(support_user)
    session.commit()

    user_to_get = User(employee_number="user007", full_name="User to Get", email="usertoget2@example.com")
    session.add(user_to_get)
    session.commit()

    with (patch('app.controllers.user_controller.get_user_by_token', return_value=support_user)):
        retrieved_user = get_user('fake_token', session, user_to_get.id)

        assert retrieved_user is None,("User should not have been retrieved"
                                       " as support_user lacks 'view_user' permission")
