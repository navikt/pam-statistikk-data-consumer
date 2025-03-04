FROM python:3.11-slim AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /job/

# Install packages to a specific directory instead of using venv
RUN pip install --upgrade pip setuptools
COPY ./job/requirements.txt /job/requirements.txt

# Install packages to a separate directory without pip/setuptools
RUN pip install --target=/job/python-packages -r requirements.txt

FROM gcr.io/distroless/python3 AS runner

# Only copy the actual packages, neither pip nor setuptools
COPY --from=builder /job/python-packages /job/python-packages
ENV PYTHONPATH="/job:/job/python-packages"
COPY ./job .
CMD ["main.py"]
