# keystone
#
# VERSION               1.0

FROM ubuntu:13.10
MAINTAINER Werner R. Mendizabal "werner.mendizabal@gmail.com"

RUN echo "deb http://archive.ubuntu.com/ubuntu saucy main universe" > /etc/apt/sources.list
RUN echo "deb-src http://archive.ubuntu.com/ubuntu saucy main universe" >> /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y python-dev libxml2-dev libxslt1-dev libsasl2-dev libsqlite3-dev libssl-dev libldap2-dev libpq-dev postgresql-client python-pip
RUN apt-get build-dep -y python-lxml

RUN pip install psycopg2

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD test-requirements.txt test-requirements.txt
RUN pip install -r test-requirements.txt

RUN apt-get install -y git python-pip make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl

RUN git clone https://github.com/yyuu/pyenv.git ~/.pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 2.7.6
RUN pyenv virtualenv 2.7.6 keystone
RUN pyenv global keystone

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt
RUN pip install psycopg2

ADD . /

RUN python setup.py develop

EXPOSE 5000 35357

ADD docstack/run.sh run.sh

CMD /run.sh
