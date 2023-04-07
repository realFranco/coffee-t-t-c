FROM alpine:3.17.2

VOLUME app
WORKDIR app

RUN apk update --no-cache && \
    apk add \
        python3=3.10.11-r0 \
        py3-pip

COPY src/requirements.txt app/requirements.txt
RUN pip3 install --no-cache-dir -r app/requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
