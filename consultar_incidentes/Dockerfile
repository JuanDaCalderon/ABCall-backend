FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

COPY __init__.py /app/__init__.py

COPY main.py /app/main.py

EXPOSE 8001

CMD ["python", "main.py"]