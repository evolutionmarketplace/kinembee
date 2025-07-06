web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn evolution_market.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A evolution_market worker --loglevel=info
beat: celery -A evolution_market beat --loglevel=info