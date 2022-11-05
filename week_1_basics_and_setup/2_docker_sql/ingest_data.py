import argparse
import pandas as pd
from sqlalchemy import create_engine  # To create the postgres engine connection
import pyarrow.parquet as pq  # For reading parquet files
import time




def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'yellow_tripdata_2021-01.csv'

    # Download parquet data from url
    df = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet')
    df = pd.read_parquet(url)
    print('Parquet has been read')
    # Export as CSV (so we can append into db using chunksize and iterator)
    df.to_csv('yellow_tripdata_2021-01.csv')

    # Create the database connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # By adding the postgres engine to the con kwarg we can output the schema in postgres format
    print(pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine))

    # Create an iterator when reading in csv
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100_000)

    # Iterate through generator. Returns first 100_000 rows
    df = next(df_iter)

    # Add the columns to the table in postgres. If anything exists overwrite it
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Add first chunk of 100_000 rows
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # iterate through the rest of the dataset above, 100_000 rows at a time
    # 1,369,769 rows so 14 chunks total
    # In a real production setting we should specify the dtypes for each column
    for idx, df_chunk in enumerate(df_iter, 2):
        start_time = time.time()
        df_chunk.to_sql(name=table_name, con=engine, if_exists='append')
        end_time = time.time()
        print(f'Chunk {idx} imported in {(end_time - start_time):.2f} seconds.\n')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user' ,help='user name for postgres')
    parser.add_argument('--password' ,help='password for postgres')
    parser.add_argument('--host' ,help='host for postgres')
    parser.add_argument('--port' ,help='port for postgres')
    parser.add_argument('--db' ,help='database name for postgres')
    parser.add_argument('--table_name' ,help='table we will write results to in postgres')
    parser.add_argument('--url' ,help='url of csv file')

    args = parser.parse_args()

    main(args)
