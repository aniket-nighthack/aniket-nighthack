FROM python:3.9.7
RUN pip install fastapi uvicorn fastapi-utils mysql-connector-python-rf passlib python-jose SQLAlchemy SQLAlchemy-Utils python-multipart
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
