release: python manage.py migrate --noinput
web: gunicorn Palachain.wsgi --bind 0.0.0.0:$PORT
