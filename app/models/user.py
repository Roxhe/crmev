from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from passlib.context import CryptContext

# Set up the password hashing context using bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """User model that represents an employee in the system."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")
    clients = relationship("Client", back_populates="sales_contact")
    contracts = relationship("Contract", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")

    def verify_password(self, password: str) -> bool:
        """
        Verify if the provided password matches the stored hashed password.

        Args:
            password (str): The plain text password to verify.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """

        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        """
        Hash the provided password and store it.

        Args:
            password (str): The plain text password to hash and store.

        Returns:
            None
        """

        self.hashed_password = pwd_context.hash(password)

    def has_permission(self, permission: str) -> bool:
        """
        Check if the user has the specified permission.

        Args:
            permission (str): The name of the permission to check.

        Returns:
            bool: True if the user has the specified permission, False otherwise.
        """

        if self.role and self.role.permissions:
            return permission in self.role.permissions.split(',')
        return False
