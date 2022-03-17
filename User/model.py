from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from Connection.database import Base
import datetime
from sqlalchemy.orm import relationship


# user table
class UsersInfo(Base):
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    hash_password = Column(String)
    mobile = Column(String)
    auth_token = Column(String)
    user_type = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)

    location = relationship("LocationInfo", uselist=True, back_populates="user")


# user loaction or city name
class LocationInfo(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String)
    city = Column(String)
    user_id = Column(Integer, ForeignKey(UsersInfo.id))

    # relationship
    user = relationship(UsersInfo, back_populates="location")
