from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    """Event model that represents an event in the system."""

    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_name = Column(String, nullable=False)
    client_contact = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    support_contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String, nullable=False)

    contract = relationship('Contract', back_populates='events')
    support_contact = relationship('User', back_populates='events')
