# Pull base image
FROM python:3.9-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip && \
    pip install pipenv
COPY Pipfile Pipfile.lock /tmp/
RUN cd /tmp && \
    pipenv install --deploy --system --ignore-pipfile
RUN useradd --create-home --home-dir /app otus

USER otus

COPY otusapp /app/
WORKDIR /app

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]