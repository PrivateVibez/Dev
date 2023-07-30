FROM python:3.9-alpine3.17

LABEL maintainer="privatevibez.com"

ENV PYTHONBUFFERED=1


COPY ./requirements.txt ./requirements.txt

COPY ./privatevibez /privatevibez

COPY ./mnt /mnt

WORKDIR /privatevibez

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser -D -H privatevibez

ENV PATH="/py/bin:$PATH"

USER privatevibez

CMD ["python", "/usr/bin/python3.py"]
