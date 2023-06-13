FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app

EXPOSE 5000

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "app.py", "--callable", "app", "--stats", "0.0.0.0:9191", "--py-autoreload", "1"]
