FROM python:3.11-alpine3.19

WORKDIR /app

COPY requirements.txt .

RUN pip install - requirements.txt
LABEL authors="Vasilis"

COPY . .

EXPOSE 8000

CMD ["python3", "-m", "flask", "run", "--host:0.0.0.0"]