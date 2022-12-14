FROM python:3.10.8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install ez_setup
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /var/run/gunicorn

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod 777 /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]