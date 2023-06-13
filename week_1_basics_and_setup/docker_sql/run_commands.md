services:
    postgres:
        image: postgres:13
        environment:
            POSTGRES_USER: airflow:
            POSTGRES_PASSWORD: airflow
            POSTGRES_DB: airflow
        volumes:
            - postgres-db-volume:/var/lib/postgresql/data
        healthcheck:
            test: ["CMD", "pg_isready", "-U", "airflow"]
            interval: 5s
            retries: 5
        restart: always


# -e -> enviornment variable flag
# volumes used for mapping folder in host machine to folder in container
# -p to map the port
# The containers network is isolated from the host machine and other networks. 
# We therefore need to explicitly specify how the container's port should be mapped to a port on the host machine
docker run -it `
    -e POSTGRES_USER="root" `
    -e POSTGRES_PASSWORD="root" `
    -e POSTGRES_DB="ny_taxi" `
    -v C:\Users\mattc\OneDrive\Documents\Data\data-engineering-zoomcamp\week_1_basics_and_setup\docker_sql\ny_taxi_postgres_data:/var/lib/postgresql/data `
    -p 5432:5432 `
    postgres:13

# https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

