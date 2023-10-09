FROM ubuntu:20.04

ENV PRELLA_LOGIN=1
ENV PRELLA_PASSWORD=1

RUN apt-get update && apt-get install -y git python3
RUN git clone https://github.com/Depard42/Prella
RUN python3 -m pip install -r Prella/requarements.txt
RUN mkdir Prella/backup

CMD ['python3', 'Prella/wsgi.py']