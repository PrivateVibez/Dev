FROM python:3.9-alpine3.17

LABEL maintainer="privatevibez.com"

ENV PYTHONBUFFERED=1


COPY ./requirements.txt ./requirements.txt

COPY ./privatevibez /privatevibez

WORKDIR /privatevibez

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # apk add --update --no-cache postgresql-client && \
    # apk add --update --no-cache --virtual .tmp-deps \
    #     build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    # apk del .tmp-deps && \
    adduser -D -H privatevibez

ENV PATH="/py/bin:$PATH"

USER privatevibez
