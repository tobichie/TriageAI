FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard ./dashboard
COPY backend/db ./db
COPY backend/app ./app

CMD ["uvicorn", "dashboard.main:app", "--host", "0.0.0.0", "--port", "8001"]
