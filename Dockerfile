FROM python:3.11-slim

LABEL authors="vladelo"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .
COPY .env .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]