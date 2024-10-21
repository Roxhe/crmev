from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    """Client model that represents a client in the system."""

    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(Date, nullable=False)
    last_contact_date = Column(Date, nullable=False)
    contact_person = Column(String, nullable=False)
    sales_contact_id = Column(Integer, ForeignKey('users.id'))

    sales_contact = relationship('User', back_populates='clients')
    contracts = relationship('Contract', back_populates='client')
