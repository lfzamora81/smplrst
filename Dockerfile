FROM alpine:latest

RUN apk add --no-cache \
    python \
    py-pip

RUN pip install \
    pymongo \
    gunicorn \
    requests \
    falcon

COPY /smplrst /smplrst

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0", "smplrst.app"]
