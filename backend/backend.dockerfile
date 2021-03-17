FROM python:3.8

RUN apt-get update
RUN apt-get install ffmpeg -y

RUN pip3 install --no-cache-dir "uvicorn[standard]" gunicorn

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app/requirements.txt /app/requirements.txt
RUN pip3 install --requirement /app/requirements.txt

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]


