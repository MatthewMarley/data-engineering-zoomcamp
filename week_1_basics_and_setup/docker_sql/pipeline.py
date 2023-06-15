# pipeline.py

import argparse
import requests
import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):

    # pandas actions
    # engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    engine = create_engine(f'postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}')
    engine.connect()

    # Read file from URL and save in cwd
    response = requests.get(params.url)
    with open('yellow_tripdata_2021-01-download.parquet', 'wb') as file:
        file.write(response.content)

    # Read parquet
    df = pd.read_parquet('yellow_tripdata_2021-01-download.parquet')

    # Convert to csv
    df.to_csv('yellow_tripdata_2021-01.csv', index=False)

    # Read back into df as an iterator object
    df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100_000)

    # First 100,000 rows
    df = next(df_iter)

    # Write column names then first 100k rows
    df.head(0).to_sql(name=f'{params.tablename}', con=engine, if_exists='replace')
    df.to_sql(name=f'{params.tablename}', con=engine, if_exists='append')

    # Loop to cycle through the rest and write in chunks
    # Iterate through the iterator, not next(iterator). The for loop will automatically call next
    for df in df_iter:
        start_chunk = time.time()
        df.to_sql(name=f'{params.tablename}', con=engine, if_exists='append')
        end_chunk = time.time()
        print(f'Chunk added to postgres. Time taken: {(end_chunk - start_chunk):.2f}s')


    print(f'Job completed successfully')


if __name__ == '__main__':
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Ingest ny_taxi data into postgres database')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--port', help='port number for postgres')
    parser.add_argument('--db', help='name of database')
    parser.add_argument('--tablename', help='name of the table in postgres db')
    parser.add_argument('--url', help='The url that the taxi data will be downloaded from')
    args = parser.parse_args()
    print(args)
    print(args.host)
    main(args)

    end_time = time.time()
    print(f'Job finished in {(end_time - start_time):.2f}s')

