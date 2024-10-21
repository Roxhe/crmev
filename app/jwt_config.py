import jwt
import datetime

# Define a secret key used for encoding and decoding JWT tokens
SECRET_KEY = 'OPENCLASSROOMP12'

def generate_token(user_id: int):
    """
    Generate a JWT token for a user.

    Args:
        user_id (int): The ID of the user for whom to generate the token.

    Returns:
        str: A JWT token encoded with the user's ID and an expiration time of 1 hour.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token: str):
    """
    Verify the validity of a JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        int or None: The user ID extracted from the token if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
