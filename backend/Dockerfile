FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD python -m alembic upgrade head && fastapi run main.py
