FROM python:3.13-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir flask==3.1.3
COPY app ./app
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
EXPOSE 8080
CMD ["python", "-m", "app.main"]
