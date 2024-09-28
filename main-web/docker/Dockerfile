FROM python:3.9

LABEL authors="Peter Bemshima, Akinyemi Sodiq"

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install the PostgreSQL client library
RUN apt-get update \
    && apt-get install -y libpq-dev wkhtmltopdf

# Copy the requirements file and install dependencies
COPY ./requirements /app/requirements

# Install dependencies
RUN pip install --no-cache-dir -r ./requirements/base.txt

# Copy the Django project code into the container

COPY ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY ./app /app

ENTRYPOINT [ "/entrypoint.sh" ]

