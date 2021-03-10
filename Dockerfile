FROM python:3.7
MAINTAINER Tianlei Wang "wangt316@myumanitoba.ca"


RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT [ "python" ]

CMD ["app.py"]