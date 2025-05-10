FROM python:3.11-slim
WORKDIR /app

ENV PYTHONPATH="/app/src"
COPY requirements.txt .
COPY src ./src

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8888

CMD ["gunicorn", "-k", "gthread", "-w", "2", "-b", "0.0.0.0:8888", "app:app"]