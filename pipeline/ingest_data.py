import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype_transactions = {
    "Purchase Price Per Unit": "float64",
    "Quantity": "float",
    "Shipping Address State": "string",
    "Title": "string",
    "ASIN/ISBN (Product Code)": "string",
    "Category": "string",
    "Survey ResponseID": "string",
}

dtype_demographics = {
    "Survey ResponseID": "string",
    "Q-demos-age": "string",
    "Q-demos-hispanic": "string",
    "Q-demos-race": "string",
    "Q-demos-education": "string",
    "Q-demos-income": "string",
    "Q-demos-gender": "string",
    "Q-sexual-orientation": "string",
    "Q-demos-state": "string",
    "Q-amazon-use-howmany": "string",
    "Q-amazon-use-hh-size": "string",
    "Q-amazon-use-how-oft": "string",
    "Q-substance-use-cigarettes": "string",
    "Q-substance-use-marijuana": "string",
    "Q-substance-use-alcohol": "string",
    "Q-personal-diabetes": "string",
    "Q-personal-wheelchair": "string",
    "Q-life-changes": "string",
    "Q-sell-YOUR-data": "string",
    "Q-sell-consumer-data": "string",
    "Q-small-biz-use": "string",
    "Q-census-use": "string",
    "Q-research-society": "string",
}

parse_dates = ["Order Date"]

@click.command()
@click.option('--dataset', type=click.Choice(['transactions', 'demographics', 'all']), default='all', help='Dataset to ingest')
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='amazon_purchases', help='PostgreSQL database name')
@click.option('--chunk-size', default=100000, type=int, help='Chunk size for reading CSV')
def run(dataset, pg_user, pg_password, pg_host, pg_port, pg_db, chunk_size):
    prefix = "https://github.com/patternlover/amazon-raw-data/releases/download/1.0.0/"
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    
    if dataset in ['transactions', 'all']:
        print("Ingesting transactions...")
        url = f"{prefix}amazon-purchases.csv.gz"
        df_iter = pd.read_csv(url, dtype=dtype_transactions, parse_dates=parse_dates, iterator=True, chunksize=chunk_size)
        first = True
        for df_chunk in tqdm(df_iter):
            if first:
                df_chunk.head(0).to_sql(name="transactions", con=engine, if_exists="replace")
                first = False
            df_chunk.to_sql(name="transactions", con=engine, if_exists="append")
        print("Transactions ingested successfully")
    
    if dataset in ['demographics', 'all']:
        print("Ingesting demographics...")
        url = f"{prefix}survey.csv.gz"
        df = pd.read_csv(url, dtype=dtype_demographics)
        df.to_sql(name="demographics", con=engine, if_exists="replace")
        print("Demographics ingested successfully")

if __name__ == '__main__':
    run()