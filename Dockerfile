# Use the Python 3.8 base image
FROM python:3.8-slim as base

# Install libpq-dev to build psycopg2
RUN apt-get update && apt-get install -y libpq-dev

# Install build tools and dependencies
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev

# Use a new stage for the build image
FROM base as build

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Use a new stage for the runtime image
FROM build as runtime

# Make port 1300 available to the world outside this container
EXPOSE 1300

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port", "1300"]