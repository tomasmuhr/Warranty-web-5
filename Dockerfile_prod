FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "1", "--threads", "1", "-b", "0.0.0.0:8000", "wsgi:create_app()"]
