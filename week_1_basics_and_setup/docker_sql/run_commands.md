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


# Access pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi

# docker command for running pgadmin
docker run -it `
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" `
    -e PGADMIN_DEFAULT_PASSWORD="root" `
    -p 8080:80 `
    dpage/pgadmin4




# docker network connect

docker network create pg-network

# name needed in order for pgadmin to discover/connect to postgres
docker run -it `
    -e POSTGRES_USER="root" `
    -e POSTGRES_PASSWORD="root" `
    -e POSTGRES_DB="ny_taxi" `
    -v C:\Users\mattc\OneDrive\Documents\Data\data-engineering-zoomcamp\week_1_basics_and_setup\docker_sql\ny_taxi_postgres_data:/var/lib/postgresql/data `
    -p 5432:5432 `
    --network=pg-network `
    --name pg-database `
    postgres:13


# Run each command one at a time. So we create the network, then add postgres container to it. Then finally add pgadmin container to it.
docker run -it `
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" `
    -e PGADMIN_DEFAULT_PASSWORD="root" `
    -p 8080:80 `
    --network=pg-network `
    dpage/pgadmin4



# run our pipeline from command line with argparse enabled
python .\pipeline.py `
    --user=root `
    --password=root `
    --host=localhost `
    --port=5432 `
    --db=ny_taxi `
    --tablename=yellow_tripdata `
    --url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"


# Build new docker container
docker build -t taxi_ingest:v001 .



# 192 means the file downloads from my localhost location
# URL2 downloads from online location
URL = "http://192.168.0.38:8000/yellow_tripdata_2021-01.parquet"
URL2 = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

# Run the new docker container, with arguments for argparse
# --network is a docker command so runs before the image name
# Then follow with all arguments for the script
docker run -it `
    --network=pg-network `
    taxi_ingest:v001 `
    --user=root `
    --password=root `
    --host=pg-database `
    --port=5432 `
    --db=ny_taxi `
    --tablename=yellow_tripdata `
    --url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    
    