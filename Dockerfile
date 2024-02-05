FROM python:3.10.12
LABEL maintainer="danielmsilverio@gmail.com"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./alembic.ini .
COPY ./entrypoint.sh .
COPY ./envs ./envs

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]