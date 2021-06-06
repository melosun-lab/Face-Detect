FROM python:3.8-slim-buster

RUN mkdir /app

COPY ./ /app

WORKDIR /app

RUN cd /app

RUN pip install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"

EXPOSE 5000

CMD ["python3", "app.py"]

