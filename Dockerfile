# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get update -y
RUN apt-get install mc -y
RUN apt-get install nfs-common -y
#RUN mount -t nfs  192.168.5.49:/share/scan_bot /mnt/

RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "Main.py"]