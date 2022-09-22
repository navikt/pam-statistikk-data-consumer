FROM navikt/python:3.8

USER root

COPY . .

RUN pip3 install -r requirements.txt

USER apprunner

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python3", "run.py"]