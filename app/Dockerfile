FROM navikt/python:3.8

USER root

COPY ./app .

WORKDIR app

RUN pip3 install -r requirements.txt

USER apprunner

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
