FROM alpine:3.17.2

VOLUME app
WORKDIR app

# python3=3.10.11-r0 \

RUN apk update --no-cache && \
    apk add \
        python3 \
        python3-dev \
        py3-pip \
        gcc \
        musl-dev \
        postgresql-libs \
        postgresql-dev

COPY app/requirements.txt app/requirements.txt
RUN pip3 install --no-cache-dir -r app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
