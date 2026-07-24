FROM python:3.12-slim

WORKDIR /app
COPY collector/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY collector/app ./app
COPY common ./common

CMD ["python", "-m", "app.main"]
