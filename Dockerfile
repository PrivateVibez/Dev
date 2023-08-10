FROM python:3.9-alpine3.17

LABEL maintainer="privatevibez.com"

ENV PYTHONBUFFERED=1


COPY ./requirements.txt ./requirements.txt

COPY ./privatevibez /privatevibez

WORKDIR /privatevibez

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt 


ENV PATH="/py/bin:$PATH"

RUN addgroup -g 1001 -S 1000 && adduser -u 1001 -S 1000 -G 1000


CMD ["python","-u", "/usr/bin/python3.py"]
