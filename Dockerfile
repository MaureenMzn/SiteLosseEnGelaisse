# Dockerfile
FROM postgis/postgis:15-3.3

RUN apt-get update && \
    apt-get install -y postgresql-15-pgrouting
