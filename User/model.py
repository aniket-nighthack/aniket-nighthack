from sqlalchemy import Column, String, Integer, DateTime
from Connection.database import Base
import datetime
# user table
class UsersInfo(Base):
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    mobile = Column(String)
    auth_token = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)