# Base image
FROM ubuntu:20.04

# Metadata as label
LABEL maintainer="privatevibez.com"

# Environment settings
ENV PYTHONBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/py/bin:$PATH"

# Update package index and install required packages
RUN apt-get update && apt-get install -y dos2unix tzdata

# Configure timezone to avoid interactive prompts
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Install essential packages, Python, and PostgreSQL client dependencies
RUN apt-get update --fix-missing && apt-get install -y \
    sudo \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    python3-pip \
    git \
    libpq-dev \
    libgdal-dev \
    libgeos-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /privatevibez

# Copy necessary files into the container
COPY ./requirements.txt ./requirements.txt
COPY ./privatevibez /privatevibez

RUN dos2unix /privatevibez/entrypoint.sh

# Set up a virtual environment and install requirements
RUN python3.9 -m venv /py && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # Installing django-cities using git
    pip install git+https://github.com/coderholic/django-cities.git

RUN chmod -R 777 /py/lib/python3.9/site-packages/cities/ && \
    chmod a+x /privatevibez/entrypoint.sh

# Expose the desired port
EXPOSE 8000

# Create a user and group
RUN groupadd -g 1001 groupname && \
    useradd -m -u 1001 -g 1001 username

# ENTRYPOINT will run as root by default, unless specified otherwise before
ENTRYPOINT [ CMD "sh", "/privatevibez/entrypoint.sh"]

# Switch to the non-root user for subsequent operations and CMD
USER username

# CMD directive for running Django's runserver for development purposes
CMD ["python3.9", "manage.py", "runserver", "0.0.0.0:8000"]
