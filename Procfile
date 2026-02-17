release: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py loadinitialdata
web: gunicorn core.wsgi --bind 0.0.0.0:$PORT