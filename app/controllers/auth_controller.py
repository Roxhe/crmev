from sqlalchemy.orm import Session
from ..models.user import User
from ..jwt_config import generate_token, verify_token


def authenticate_user(session: Session, employee_number: str, password: str):
    """
    Authenticate a user by verifying their employee number and password.

    Args:
        session (Session): The database session to use for querying.
        employee_number (str): The employee number of the user.
        password (str): The plain text password provided by the user.

    Returns:
        str or None: A JWT token if authentication is successful, None otherwise.
    """

    user = session.query(User).filter(User.employee_number == employee_number).first()
    if user and user.verify_password(password):
        token = generate_token(user.id)
        return token
    return None


def get_user_by_token(session: Session, token: str):
    """
    Retrieve a user from the database using a JWT token.

    Args:
        session (Session): The database session to use for querying.
        token (str): The JWT token to verify.

    Returns:
        User or None: The user associated with the token if valid, None otherwise.
    """

    user_id = verify_token(token)
    if user_id:
        return session.query(User).filter(User.id == user_id).first()
    return None


def user_has_permission(user: User, permission: str):
    """
    Check if the user has the specified permission.

    Args:
        user (User): The user to check the permissions for.
        permission (str): The name of the permission to check.

    Returns:
        bool: True if the user has the specified permission, False otherwise.
    """

    if not user or not user.role:
        return False
    return permission in user.role.permissions.split(',')
