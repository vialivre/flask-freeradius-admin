FROM python:3.6-alpine

RUN adduser -D freeradius_admin

WORKDIR /home/flask-freeradius-admin

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  venv/bin/pip install -r requirements.txt --no-cache-dir && \
  venv/bin/pip install gunicorn --no-cache-dir && \
  apk --purge del .build-deps

COPY . ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R freeradius_admin:freeradius_admin ./
USER freeradius_admin

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]