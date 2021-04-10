web: gunicorn hillel_post.wsgi --log-file -
worker: celery -A hillel_post.celery worker -B --log-file -