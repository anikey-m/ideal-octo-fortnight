FROM python:latest

ADD requirements-uwsgi-pg.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

ADD store/ /app/store
ADD order/ /app/order
ADD manage.py /app/manage.py

ENV DJANGO_SETTINGS_MODULE=store.settings
WORKDIR /app

EXPOSE 8000

CMD ["uwsgi", "--chdir=/app", "--module=store.wsgi:application", "--master", "--pidfile=/tmp/project-master.pid", "--http=0.0.0.0:8000", "--process=5", "--harakiri=30", "--max-requests=5000", "--vacuum", "--static-map", "/static=/app/static"]
