FROM python:latest 
USER root

RUN apt-get update \
    && apt-get install -y mecab \
    && apt-get install -y libmecab-dev \
    && apt-get install -y mecab-ipadic-utf8\
    && apt-get install -y git\
    && apt-get install -y make\
    && apt-get install -y curl\
    && apt-get install -y xz-utils\
    && apt-get install -y file\
    && apt-get install -y sudo\
    && apt-get install -y wget


RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git\
    && cd mecab-ipadic-neologd\
    && bin/install-mecab-ipadic-neologd -n -y

RUN pip install numpy
RUN pip install pandas
RUN pip install sklearn
RUN pip install gensim
RUN pip install mecab-python3==0.996.5
RUN pip install python-dotenv
RUN pip install bs4
RUN pip install pykakasi
RUN pip install nlplot
