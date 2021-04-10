web: gunicorn hillel_post.wsgi --log-file -
worker: python manage.py celery worker -B -l info