import click
from functools import wraps
import jwt
from models.user import User
from jwt_config import SECRET_KEY
from sqlalchemy.orm import sessionmaker
from init_db import engine
from views.auth_view import load_token_from_ini

# Create a new database session
Session = sessionmaker(bind=engine)
session = Session()

def get_user_from_token(token):
    """
    Decode the JWT token to retrieve the user associated with it.

    Args:
        token (str): The JWT token to decode.

    Returns:
        User: The user associated with the token.

    Raises:
        PermissionError: If the user is not found in the database, the token is expired, or the token is invalid.
    """
    try:
        # Decode the token to get user information
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get('user_id')
        # Query the user from the database
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise PermissionError("User not found in the database.")
        click.echo(f"User found: {user.full_name}")
        return user
    except jwt.ExpiredSignatureError:
        raise PermissionError("Token has expired.")
    except jwt.InvalidTokenError:
        raise PermissionError("Invalid token.")

def load_token(f):
    """
    Decorator to load the authentication token from the configuration file.

    Args:
        f (function): The function to be wrapped by the decorator.

    Returns:
        function: The wrapped function with the loaded user.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Load the token from the INI file
        token = load_token_from_ini()
        if not token:
            click.echo("No user is currently logged in. Please log in first.")
            return
        try:
            # Get the user associated with the token
            user = get_user_from_token(token)
        except PermissionError as e:
            click.echo(str(e))
            return
        # Call the original function with the authenticated user
        return f(user, *args, **kwargs)

    return wrapper
