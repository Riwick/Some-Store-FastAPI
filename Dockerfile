FROM python:3.12-alpine

WORKDIR /fastapi_app

COPY req.txt /fastapi_app

RUN pip install -r req.txt

COPY . /fastapi_app

RUN chmod a+x docker/*.sh

#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000