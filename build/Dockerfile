FROM ubuntu:20.04
MAINTAINER Depard42

EXPOSE 80

#ENV PRELLA_LOGIN=1
#ENV PRELLA_PASSWORD=1

RUN apt-get update && apt-get install -y git python3 python3-pip
RUN git clone https://github.com/Depard42/Prella
WORKDIR /Prella

RUN pip3 install -r requarements.txt
RUN mkdir backup

CMD [ "python3", "wsgi.py" ]