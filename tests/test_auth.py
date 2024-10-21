from app.controllers.auth_controller import authenticate_user, get_user_by_token, user_has_permission
from app.models.user import User
from app.models.role import Role
from app.jwt_config import generate_token


def test_authenticate_user_valid(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    user = User(employee_number='valid_user', full_name='Valid User', email='valid@example.com', role=role)
    user.set_password('valid_password')
    session.add(user)
    session.commit()

    token = authenticate_user(session, employee_number='valid_user', password='valid_password')

    assert token is not None, "Token should be generated for valid credentials"


def test_authenticate_user_invalid_password(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    user = User(employee_number='valid_user', full_name='Valid User', email='valid@example.com', role=role)
    user.set_password('valid_password')
    session.add(user)
    session.commit()

    token = authenticate_user(session, employee_number='valid_user', password='wrong_password')

    assert token is None, "Token should not be generated for invalid password"


def test_authenticate_user_invalid_user(session):
    token = authenticate_user(session, employee_number='invalid_user', password='any_password')

    assert token is None, "Token should not be generated for non-existent user"


def test_get_user_by_token_valid(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    user = User(employee_number='valid_user', full_name='Valid User', email='valid@example.com', role=role)
    session.add(user)
    session.commit()

    token = generate_token(user.id)

    retrieved_user = get_user_by_token(session, token=token)

    assert retrieved_user is not None, "User should be retrieved for a valid token"
    assert retrieved_user.id == user.id, "Retrieved user ID should match the original user ID"


def test_get_user_by_token_invalid(session):
    retrieved_user = get_user_by_token(session, token='invalid_token')

    assert retrieved_user is None, "User should not be retrieved for an invalid token"


def test_user_has_permission_with_permission(session):
    role = session.query(Role).filter_by(role_name='Gestion').first()
    if not role:
        role = Role(role_name='Gestion', permissions='create_client,view_client,delete_user')
        session.add(role)
        session.commit()

    user = User(employee_number='admin001', full_name='Admin User', email='admin@example.com', role=role)
    session.add(user)
    session.commit()

    has_permission = user_has_permission(user, 'create_client')

    assert has_permission, "User should have 'create_client' permission"


def test_user_has_permission_without_permission(session):
    role = Role(role_name='Gestion Test', permissions='view_client,delete_user')
    session.add(role)
    session.commit()

    user = User(employee_number='admin002', full_name='Admin User', email='admin2@example.com', role=role)
    session.add(user)
    session.commit()

    has_permission = user_has_permission(user, 'create_client')

    assert not has_permission, "User should not have 'create_client' permission"


def test_user_has_permission_no_role(session):
    user = User(employee_number='user003', full_name='No Role User', email='norole@example.com', role=None)
    session.add(user)
    session.commit()

    has_permission = user_has_permission(user, 'create_client')

    assert not has_permission, "User without a role should not have any permissions"


def test_user_has_permission_no_user():
    has_permission = user_has_permission(None, 'create_client')

    assert not has_permission, "None user should not have any permissions"
