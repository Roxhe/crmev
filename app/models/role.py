from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Role(Base):
    """Role model that represents user roles in the system."""

    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False, unique=True)
    permissions = Column(String, nullable=False)

    users = relationship('User', back_populates='role')
