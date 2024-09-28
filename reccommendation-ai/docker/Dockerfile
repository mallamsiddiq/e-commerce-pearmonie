FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements/base.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code

# Expose the Flask port
EXPOSE 5000

# Command to run the application
# CMD ["python", "run.py"]

COPY ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY . .

ENTRYPOINT [ "/entrypoint.sh" ]

