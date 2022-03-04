from sqlalchemy import Column, String, ForeignKey,Integer, DateTime, Time, Boolean
from Connection.database import Base
import datetime
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship

# theters info
class ThetersInfo(Base):
    __tablename__ = 'theter'

    id = Column(Integer, primary_key=True, index=True)
    t_name = Column(String)
    t_address = Column(String)
    t_contact = Column(String)
    opening_time = Column(String)
    closing_time = Column(String)
    auth_token = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)

    docs = relationship("TheterDocsInfo",uselist=True, back_populates="theter")
    verification = relationship("TheterVerificationInfo", uselist=True, back_populates="theter")
    screens = relationship("TheterScreenInfo", uselist=True, back_populates="theter")

# theter documents model
class TheterDocsInfo(Base):
    __tablename__ = 'theter_docs'

    id = Column(Integer, primary_key=True, index=True)
    shop_act_licence = Column(String)
    gst_licence = Column(String)
    tid = Column(Integer, ForeignKey("theter.id"))

    theter = relationship("ThetersInfo", back_populates="docs")

#  theter verification model
class TheterVerificationInfo(Base):
    __tablename__ = 'theter_verification'

    id = Column(Integer, primary_key=True, index=True)
    shopact_verify = Column(Boolean)
    gst_verify = Column(Boolean)
    is_live = Column(Boolean)
    is_verifyed = Column(Boolean)
    tid = Column(Integer, ForeignKey("theter.id"))
    create_at = Column(DateTime, default=datetime.datetime.utcnow)

    theter = relationship("ThetersInfo", back_populates="verification")

# thetr screen model
class TheterScreenInfo(Base):
    __tablename__ = 'screens'

    id = Column(Integer, primary_key=True, index=True)
    screen_type = Column(String)
    tid = Column(Integer, ForeignKey("theter.id"))
    theter = relationship("ThetersInfo", back_populates="screens")
    seats = relationship("SeatsInfo", uselist=True ,back_populates="screen")

# screen seats
class SeatsInfo(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    tid = Column(Integer, ForeignKey("theter.id"))
    seat_name = Column(String)
    seat_price = Column(Integer)
    screenid = Column(Integer, ForeignKey("screens.id"))
    seat_status = Column(Boolean)

    screen = relationship("TheterScreenInfo", back_populates="seats")
