# Postgres base image
FROM postgres

# Copy init scripts
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose default port for postgres
EXPOSE 5432
