from sqlalchemy import Column, String, Integer, DateTime, Time
from Connection.database import Base
import datetime

# theters info
class ThetersInfo(Base):
    __tablename__ = 'theter'

    id = Column(Integer, primary_key=True, index=True)
    t_name = Column(String)
    t_address = Column(String)
    t_contact = Column(String)
    auth_token = Column(String)
    opening_time = Column(String)
    closing_time = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
