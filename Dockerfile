FROM python:3.7-buster

MAINTAINER Cesar Bragagnini <cesarbrma91@gmail.com>

RUN mkdir /usr/credit-risk
COPY . /usr/credit-risk

RUN pip3 install --upgrade pip
RUN pip install -r /usr/credit-risk/credit-risk-API/requirements.txt

EXPOSE 6924

WORKDIR /usr/credit-risk/credit-risk-API
CMD ["python","server.py"]