from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Contract(Base):
    """Contract model that represents a contract in the system."""

    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    sales_contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    creation_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    client = relationship('Client', back_populates='contracts')
    sales_contact = relationship('User', back_populates='contracts')
    events = relationship('Event', back_populates='contract')
