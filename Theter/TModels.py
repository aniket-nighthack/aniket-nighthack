from sqlalchemy import Column, String, ForeignKey,Integer, DateTime, Time, Boolean
from Connection.database import Base
import datetime
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship
from User.model import UsersInfo

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
    screens = relationship("TheterScreenInfo",  uselist=True, back_populates="theter")

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
    show = relationship('ShowsInfo', uselist=True )
# screen seats
class SeatsInfo(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    tid = Column(Integer)
    seat_name = Column(String)
    seat_price = Column(Integer)
    seat_status = Column(Boolean)
    screenid = Column(Integer, ForeignKey("screens.id"))
    screen = relationship(TheterScreenInfo, foreign_keys=[screenid])

# movie model
class MovieInfo(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    mov_name = Column(String)
    language = Column(String)
    mov_type = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)


# current shows model   
class ShowsInfo(Base):
    __tablename__ = 'shows'

    id = Column(Integer, primary_key=True, index=True)
    # tid = Column(Integer)
    tid = Column(Integer, ForeignKey(ThetersInfo.id))
    screenid = Column(ForeignKey(TheterScreenInfo.id))
    start_time = Column(String)
    end_time = Column(String)
    mid = Column(Integer, ForeignKey(MovieInfo.id))
    available_seats = Column(Integer)
    book_seats = Column(Integer)
    show_type = Column(Boolean)
    show_ticket = Column(Integer)
    show_date = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)

    screens = relationship(TheterScreenInfo, uselist=True, foreign_keys=[screenid])
    movie = relationship(MovieInfo, uselist=True,  foreign_keys=[mid])
    theter = relationship(ThetersInfo, uselist=True,foreign_keys=[tid])

    # show = relationship("BookingInfo", back_populates="showdetails")

# booking a shows       
class BookingInfo(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, index=True)
    showid = Column(Integer, ForeignKey(ShowsInfo.id))
    seatid = Column(Integer, ForeignKey(SeatsInfo.id))
    booking_slot = Column(String)
    booking_date = Column(String)
    uid = Column(Integer, ForeignKey(UsersInfo.id))
    create_at = Column(DateTime, default=datetime.datetime.utcnow)

    showdetails = relationship(ShowsInfo,uselist=True, foreign_keys=[showid])