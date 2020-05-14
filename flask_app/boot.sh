#!/bin/sh
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b 0.0.0.0:5000 -b [::0]:5000 --access-logfile /var/log/flask_freeradius_admin/access.log --error-logfile /var/log/flask_freeradius_admin/status.log app:app