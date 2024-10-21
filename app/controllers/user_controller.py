from sqlalchemy.orm import Session
from ..models.user import User
from ..models.role import Role
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
def create_user(token: str, session: Session, employee_number: str, password: str, email: str,
                full_name: str, department: str, role_name: str):
    """
    Create a new user in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        employee_number (str): The unique employee number for the user.
        password (str): The plain text password for the user.
        email (str): The email address of the user.
        full_name (str): The full name of the user.
        department (str): The department where the user works.
        role_name (str): The name of the role to assign to the user.

    Returns:
        User or None: The created user object if successful, None otherwise.

    Raises:
        ValueError: If the specified role does not exist.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('create_user'):
        return None

    role = session.query(Role).filter_by(role_name=role_name).first()
    if not role:
        raise ValueError(f"Role {role_name} does not exist")

    new_user = User(
        employee_number=employee_number,
        email=email,
        full_name=full_name,
        department=department,
        role=role
    )
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    return new_user

"""READ"""
def get_user(token: str, session, user_id: int):
    """
    Retrieve a user from the database by their ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User or None: The user object if found and permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_user'):
        return None

    return session.query(User).filter(User.id == user_id).first()


def get_all_users(user, session):
    """
    Retrieve all users from the database.

    Args:
        user (User): The user requesting the information.
        session (Session): The database session to use for querying.

    Returns:
        list[User]: A list of all user objects.

    Raises:
        PermissionError: If the user does not have permission to view all users or if the user is invalid.
    """

    if not user:
        raise PermissionError("User is not valid or not logged in.")
    if not user.has_permission('view_all'):
        raise PermissionError("You do not have permission to view all users.")
    return session.query(User).all()

"""UPDATE"""
def update_user(token: str, session: Session, user_id: int, username: str = None, password: str = None,
                email: str = None, full_name: str = None, department: str = None, role_name: str = None):
    """
    Update an existing user in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        user_id (int): The ID of the user to update.
        username (str, optional): The new username for the user.
        password (str, optional): The new password for the user.
        email (str, optional): The new email address for the user.
        full_name (str, optional): The new full name of the user.
        department (str, optional): The new department of the user.
        role_name (str, optional): The new role name for the user.

    Returns:
        User or None: The updated user object if successful, None otherwise.

    Raises:
        ValueError: If the user or specified role does not exist.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('update_user'):
        return None

    user_to_update = session.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise ValueError(f"User with id {user_id} does not exist")

    if username:
        user_to_update.username = username
    if password:
        user_to_update.set_password(password)
    if email:
        user_to_update.email = email
    if full_name:
        user_to_update.full_name = full_name
    if department:
        user_to_update.department = department
    if role_name:
        role = session.query(Role).filter_by(role_name=role_name).first()
        if not role:
            raise ValueError(f"Role {role_name} does not exist")
        user_to_update.role = role

    session.commit()
    return user_to_update

"""DELETE"""
def delete_user(token: str, session: Session, user_id: int):
    """
    Delete a user from the database by their ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        user_id (int): The ID of the user to delete.

    Returns:
        User or None: The deleted user object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('delete_user'):
        return None

    user_to_delete = session.query(User).filter_by(id=user_id).first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        return user_to_delete

    return None
