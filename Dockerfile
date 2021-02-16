FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update

RUN pip install pymongo

COPY ./main.py /app