# Frontend
FROM node:14 as build-stage

COPY ./frontend /vue
WORKDIR /vue
RUN npm install && npm run build


# Backend
FROM python:3.8

RUN apt-get update
RUN apt-get install ffmpeg -y

RUN pip3 install --no-cache-dir "uvicorn[standard]" gunicorn

COPY ./backend/start.sh /start.sh
RUN chmod +x /start.sh
COPY ./backend/gunicorn_conf.py /gunicorn_conf.py

COPY ./backend/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./backend/app/requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists
RUN pip3 install --requirement /app/requirements.txt

COPY --from=build-stage /vue/dist /vue

COPY ./backend/app /app
ENV PYTHONPATH=/app

CMD ["/start.sh"]

# docker run -d --name fastapi-youtubedl-vue --env-file .env -e MAX_WORKERS=2 -e PORT=6696 -p 6696:6696 -v /youtube-dl:/youtube-dl  fastapi-youtubedl-vue

