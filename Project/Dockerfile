FROM python:3.9-slim-buster

WORKDIR /app/db

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "unittest", "test_App.py" ]