FROM python:3.9-slim-buster

RUN set -ex \
    && pip3 install zeroconf

COPY script.py ./

ENTRYPOINT [ "python3", "-u", "./script.py" ]