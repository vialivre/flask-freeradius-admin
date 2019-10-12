FROM python:3.6-alpine

RUN adduser -D freeradius_admin

WORKDIR /home/flask-freeradius-admin

COPY . ./

RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  pip install -r requirements.txt --no-cache-dir && \
  pip install gunicorn --no-cache-dir && \
  apk --purge del .build-deps

RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R freeradius_admin:freeradius_admin ./
RUN mkdir /var/log/flask_freeradius_admin
RUN chown -R freeradius_admin:freeradius_admin /var/log/flask_freeradius_admin
USER freeradius_admin

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]