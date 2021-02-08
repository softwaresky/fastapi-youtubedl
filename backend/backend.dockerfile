#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
#
#WORKDIR /app/
#
## Install Poetry
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#    cd /usr/local/bin && \
#    ln -s /opt/poetry/bin/poetry && \
#    poetry config virtualenvs.create false
#
## Copy poetry.lock* in case it doesn't exist in the repo
#COPY ./app/pyproject.toml ./app/poetry.lock* /app/
#
## Allow installing dev dependencies to run tests
#ARG INSTALL_DEV=false
#RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
#
## For development, Jupyter remote kernel, Hydrogen
## Using inside the container:
## jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
#ARG INSTALL_JUPYTER=false
#RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"
#
#COPY ./app /app
#ENV PYTHONPATH=/app


#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
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
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5678"]