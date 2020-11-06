FROM python:3.7-slim

COPY forwarder.py /app/forwarder.py

RUN pip3 install paho-mqtt click

ENTRYPOINT ["python3", "-u", "/app/forwarder.py"]
