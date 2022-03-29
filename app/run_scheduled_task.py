from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, joinedload
import secrets
from app.Common.APIResponses import Responses
from typing import List
from app.Theter.TModels import *
from app.Theter.TSchemas import *
from app.Common.Helper import *
from app.Theter.TExceptions import *
from fastapi import HTTPException
from sqlalchemy.sql.expression import func, case
from sqlalchemy.sql.expression import false, true
from app.Theter.cruds.Theters import *
from app.Theter.cruds.seats import *
from datetime import date
from datetime import timedelta
from app.Connection.database import *

session = SessionLocal()


def clear_old_movie():
    today = date.today()
    yesterday = today - timedelta(days=1)
    data = session.query(ShowsInfo).filter(ShowsInfo.show_date == yesterday, ShowsInfo.show_type == True).all()

    if data:
        for i in data:
            i.show_type = False
            session.add(i)
            session.commit()

    print("scheduled_task ->show updated")
