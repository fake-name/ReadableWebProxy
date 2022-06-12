
FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y --no-install-recommends sudo
RUN adduser --disabled-password --gecos '' scrapeworker
RUN mkdir -p /home/scrapeworker && chown -R scrapeworker:scrapeworker /home/scrapeworker
RUN usermod -aG sudo scrapeworker
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER scrapeworker

COPY . /app

RUN ls -lah /app
RUN du /app --max-depth=1


RUN sudo apt-get update

RUN echo 'tzdata tzdata/Areas select America'             | sudo debconf-set-selections
RUN echo 'tzdata tzdata/Zones/America select Los_Angeles' | sudo debconf-set-selections

RUN DEBIAN_FRONTEND="noninteractive" sudo apt-get install --no-install-recommends -y tzdata
RUN DEBIAN_FRONTEND="noninteractive" sudo apt-get install --no-install-recommends -y build-essential libfontconfig libxml2 \
                      libxml2-dev libxslt1-dev python3-dev libz-dev zlib1g-dev libxml2-dev libxslt-dev git postgresql-common \
                      libpq-dev libunwind-dev
RUN DEBIAN_FRONTEND="noninteractive" sudo apt-get install --no-install-recommends -y python3-pip


RUN sudo pip3 install --upgrade -r /app/requirements.txt


# CMD python /app/app.py