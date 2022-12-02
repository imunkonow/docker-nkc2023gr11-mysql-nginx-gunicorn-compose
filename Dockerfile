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

COPY ./startup.sh /usr/src/app/startup.sh
RUN chmod 744 /usr/src/app/startup.sh
CMD ["/usr/src/app/startup.sh"]
# CMD ["gunicorn", "mysite.wsgi", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]
