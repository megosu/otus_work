# Pull base image
FROM python:3.9-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV USER otus
ENV HOME_DIR /otusapp
ENV WORK_DIR /otusapp/otusapp

# Install dependencies
RUN apt update && \
    apt install -y build-essential default-libmysqlclient-dev
RUN pip install --upgrade pip && \
    pip install pipenv
COPY Pipfile Pipfile.lock /tmp/
RUN cd /tmp && \
    pipenv install --deploy --system --ignore-pipfile
RUN useradd --create-home --home-dir "${HOME_DIR}" "${USER}"

USER "${USER}"

WORKDIR '${HOME_DIR}'
COPY . .

EXPOSE 8000
CMD [ "uvicorn", "otusapp.main:app", "--host", "0.0.0.0", "--port", "8000" ]