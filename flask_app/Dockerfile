FROM python:3.6-alpine

RUN adduser -D freeradius_admin

WORKDIR /home/flask-freeradius-admin

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY . ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R freeradius_admin:freeradius_admin ./
USER freeradius_admin

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]