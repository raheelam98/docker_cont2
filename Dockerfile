# step1:- Use an official Python runtime as a parent image
FROM python:3.12

# step2:- Set the working directory in the container
WORKDIR /code

# step3:- Set environments, Install Poetry
RUN pip install poetry

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# step-extra-1 :- 
# ./pyproject.toml (current directory on the host machine) 
# ./api_images/code/ (destination path within the Docker image)
# COPY file "pyproject.toml" from current location to a folder "/api_images/code/" in the Docker image being created.
COPY ./pyproject.toml /code/

#COPY .docker_con1 /code/docker_con1

# setp4:- Install dependencies including development 
RUN poetry install

# note:- Configuration to avoid creating virtual environments inside the Docker container
# poetry config virtualenvs.create false

# step5:-  Copy the current directory contents into the container at /code
COPY . /code/


# Make port 8000 available to the world outside this container
EXPOSE 8000

# sept6:- Run the app. CMD can be overridden when starting the container
CMD ["poetry", "run", "uvicorn", "docker_con1.route:app", "--host", "0.0.0.0", "--reload"]
