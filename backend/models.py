from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    company = Column(String)
    category = Column(String)
    status = Column(String, default="new")
    first_email_date = Column(DateTime)
