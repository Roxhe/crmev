from sqlalchemy.orm import Session
from ..models.contract import Contract
from ..models.user import User
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
def create_contract(token: str, session: Session, client_id, sales_contact_id,
                    total_amount, amount_due, creation_date, status):
    """
    Create a new contract in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        client_id (int): The ID of the client associated with the contract.
        sales_contact_id (int): The ID of the sales contact responsible for the contract.
        total_amount (float): The total amount of the contract.
        amount_due (float): The amount due for the contract.
        creation_date (Date): The date when the contract was created.
        status (str): The status of the contract.

    Returns:
        Contract or None: The created contract object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('create_contract'):
        return None

    new_contract = Contract(
        client_id=client_id,
        sales_contact_id=sales_contact_id,
        total_amount=total_amount,
        amount_due=amount_due,
        creation_date=creation_date,
        status=status
    )
    session.add(new_contract)
    session.commit()
    return new_contract

"""READ"""
def get_contract(token: str, session: Session, contract_id: int):
    """
    Retrieve a contract from the database by its ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.
        contract_id (int): The ID of the contract to retrieve.

    Returns:
        Contract or None: The contract object if found and permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_contract'):
        return None

    return session.query(Contract).filter(Contract.id == contract_id).first()


def get_all_contracts(token: str, session: Session, signed_only=False, unpaid_only=False):
    """
    Retrieve all contracts from the database, with optional filters.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying.
        signed_only (bool, optional): If True, only retrieve signed contracts.
        unpaid_only (bool, optional): If True, only retrieve contracts with an outstanding balance.

    Returns:
        list[Contract] or None: A list of contract objects if permissions are valid, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('view_contract'):
        return None

    query = session.query(Contract)

    if signed_only:
        query = query.filter(Contract.status == 'Signed')
    if unpaid_only:
        query = query.filter(Contract.amount_due > 0)

    return query.all()

"""UPDATE"""
def update_contract(token: str, session: Session, contract_id, sales_contact_id=None,
                    total_amount=None, amount_due=None, status=None):
    """
    Update an existing contract in the database.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        contract_id (int): The ID of the contract to update.
        sales_contact_id (int, optional): The new sales contact ID for the contract.
        total_amount (float, optional): The new total amount for the contract.
        amount_due (float, optional): The new amount due for the contract.
        status (str, optional): The new status of the contract.

    Returns:
        Contract or None: The updated contract object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('update_contract'):
        return None

    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    if contract:
        if sales_contact_id:
            contract.sales_contact_id = sales_contact_id
        if total_amount:
            contract.total_amount = total_amount
        if amount_due:
            contract.amount_due = amount_due
        if status is not None:
            contract.status = status
        session.commit()
        return contract

    return None

"""SIGN CONTRACT"""
def sign_contract(token: str, session: Session, contract_id: int):
    """
    Sign a contract by updating its status to 'Signed'.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        contract_id (int): The ID of the contract to sign.

    Raises:
        PermissionError: If the user does not have permission to sign contracts.
        ValueError: If the contract is not found or if it is already signed.

    Returns:
        Contract: The signed contract object.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('sign_contract'):
        raise PermissionError("You do not have permission to sign contracts.")

    contract = session.query(Contract).filter_by(id=contract_id).first()

    if not contract:
        raise ValueError(f"Contract with ID {contract_id} not found.")
    if contract.status == 'Signed':
        raise ValueError(f"Contract {contract_id} is already signed.")

    contract.status = 'Signed'
    session.commit()
    return contract

"""DELETE"""
def delete_contract(token: str, session: Session, contract_id):
    """
    Delete a contract from the database by its ID.

    Args:
        token (str): The JWT token to verify the user's identity and permissions.
        session (Session): The database session to use for querying and committing changes.
        contract_id (int): The ID of the contract to delete.

    Returns:
        Contract or None: The deleted contract object if successful, None otherwise.
    """

    user = get_user_by_token(session, token)

    if not user.has_permission('delete_contract'):
        return None

    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    if contract:
        session.delete(contract)
        session.commit()
        return contract

    return None
