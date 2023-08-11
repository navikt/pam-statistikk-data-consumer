FROM ghcr.io/navikt/baseimages/python:3.11

USER root
RUN unset https_proxy
COPY ./job .

RUN pip3 install -r requirements.txt

CMD python3 main.py
