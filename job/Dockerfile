FROM navikt/python:3.8

USER root

COPY ./job .

RUN pip3 install -r requirements.txt

CMD python3 main.py
