#!/bin/sh

set -e # -e flag will cause the script to exit immediately if a simple command exits with a nonzero exit value

python manage.py wait_for_db
python manage.py collectstatic --noinput # collect all static files into a single directory
python manage.py migrate

# --socket :9000: uWSGI will listen on port 9000
# --workers 4: uWSGI will start 4 worker processes
# --master: uWSGI will start a master process
# --enable-threads: uWSGI will enable threading, so multiple requests can be handled concurrently
# --module app.wsgi: tells uWSGI where is the entry point of the application (wsgi.py file)
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
