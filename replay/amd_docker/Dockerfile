FROM brewblox/brewblox-service:latest

WORKDIR replay

COPY ./* ./

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "replay.py"]
