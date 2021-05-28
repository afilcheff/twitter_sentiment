FROM python:3

WORKDIR /app

COPY /src /app

RUN pip install -r /app/requirements.txt

CMD python3 /app/stream.py