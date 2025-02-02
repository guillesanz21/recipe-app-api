FROM python:3.9-alpine3.13
# Good practice to inform to other developers who created and mantains the container
LABEL maintainer="guillesanz21"

# Recommended when you run Python in a Docker container. It tells Python that you don't want to buffer the output.
# The output from Python will be printed directly to the console, which prevents any delays of messages.
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /usr/app
WORKDIR /usr/app
EXPOSE 8000

# Default to false. But if this containers is run through docker-compose, it will be overwritted to true. This means that docker-compose will used in development.
ARG DEV=false

# RUN python -m venv /py || Create a python virtual environment inside the container to avoid edge-cases
#   when a dependency defaulty installed conflicts with another specified in the requirements.txt
# RUN pip install --upgrade pip || Updates pip (but only for the virtual environemnt)
# RUN apk add ... build-base ... || Dependencies needed in order to install the postgreSQL adaptor
# RUN adduser - Add django user (it is best practice not to use the root user)
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # Cleaning
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

RUN chown -R django-user:django-user /usr/app

USER django-user