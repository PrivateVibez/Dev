FROM ubuntu:20.04

LABEL maintainer="privatevibez.com"

ENV PYTHONBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/py/bin:$PATH"

# Configure timezone to avoid interactive prompts later
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Install essential packages and Python
RUN apt-get update --fix-missing && apt-get install -y \
    python3.9 \
    python3.9-venv \
    python3-pip \
    git \
    libsqlite3-mod-spatialite \
    spatialite-bin \
    libgdal-dev \
    libgeos-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /privatevibez

# Copy necessary files into the container
COPY ./requirements.txt ./requirements.txt
COPY ./privatevibez /privatevibez

# Set up a virtual environment and install requirements
RUN python3.9 -m venv /py && \
    pip install --upgrade pip && \
    pip install -r requirements.txt 

# Installing django-cities using git
RUN pip install git+https://github.com/coderholic/django-cities.git

# Expose the desired port
EXPOSE 8000

# Create a user and group, and switch to that user
RUN groupadd -g 1001 groupname && \
    useradd -m -u 1001 -g 1001 username && \
    chmod 776 db.sqlite3 && \
    chown username:groupname db.sqlite3

USER username


# CMD directive for running Django's runserver for development purposes
CMD ["python3.9", "manage.py", "runserver", "0.0.0.0:8000"]
