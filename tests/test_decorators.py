import pytest
from unittest.mock import patch, MagicMock
from app.decorators import get_user_from_token, load_token
from app.models.user import User
import jwt
from app.jwt_config import SECRET_KEY

def test_get_user_from_token_valid_user(session):
    user = User(id=1, full_name='Valid User', email='valid@example.com')
    session.add(user)
    session.commit()

    token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm="HS256")

    with patch('app.decorators.session', session):
        retrieved_user = get_user_from_token(token)
        assert retrieved_user is not None, "User should be retrieved for a valid token"
        assert retrieved_user.id == user.id, "Retrieved user ID should match the original user ID"

def test_get_user_from_token_user_not_found():
    token = jwt.encode({'user_id': 999}, SECRET_KEY, algorithm="HS256")

    with pytest.raises(PermissionError, match="User not found in the database."):
        get_user_from_token(token)

def test_get_user_from_token_expired():
    expired_token = jwt.encode({'user_id': 1, 'exp': 0}, SECRET_KEY, algorithm="HS256")

    with pytest.raises(PermissionError, match="Token has expired."):
        get_user_from_token(expired_token)

def test_get_user_from_token_invalid():
    invalid_token = "invalid.token.signature"

    with pytest.raises(PermissionError, match="Invalid token."):
        get_user_from_token(invalid_token)

@pytest.mark.usefixtures("session")
@patch('app.views.auth_view.load_token_from_ini')
@patch('app.decorators.get_user_from_token')
@patch('app.decorators.session', autospec=True)
def test_load_token_valid_token(mock_session, mock_get_user_from_token, mock_load_token_from_ini, session):
    mock_load_token_from_ini.return_value = "valid_token"
    mock_user = MagicMock()
    mock_user.full_name = "Mock User"
    mock_get_user_from_token.return_value = mock_user

    mock_session.return_value = session

    @load_token
    def decorated_function(user):
        return f"Hello, {user.full_name}"

    result = decorated_function()

    assert result == f"Hello, {mock_user.full_name}", "The decorated function should return a greeting for the user"

@patch('views.auth_view.load_token_from_ini')
def test_load_token_no_token(mock_load_token_from_ini):
    mock_load_token_from_ini.return_value = None

    @load_token
    def decorated_function(user):
        return "This should not be called"

    result = decorated_function()

    assert result is None, "The decorated function should not be called if no token is found"

@patch('views.auth_view.load_token_from_ini')
@patch('decorators.get_user_from_token')
def test_load_token_invalid_token(mock_get_user_from_token, mock_load_token_from_ini):
    mock_load_token_from_ini.return_value = "invalid_token"

    mock_get_user_from_token.side_effect = PermissionError("Invalid token.")

    @load_token
    def decorated_function(user):
        return "This should not be called"

    result = decorated_function()

    assert result is None, "The decorated function should not be called if the token is invalid"
