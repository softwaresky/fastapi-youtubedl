FROM python:3.8

WORKDIR /app/

RUN pip install fastapi uvicorn

COPY ./app/requirements.txt /app/requirements.txt
#RUN python3 -m pip install --upgrade pip
#RUN pip3 install --upgrade setuptools
RUN pip install --requirement /app/requirements.txt

EXPOSE 5678

ENV PYTHONPATH=/app
COPY ./app /app

#CMD uvicorn app.main:app --host 127.0.0.1 --port 5678
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5678"]