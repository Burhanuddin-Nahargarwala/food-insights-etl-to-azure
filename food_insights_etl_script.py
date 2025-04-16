import requests
import pandas as pd
from sqlalchemy import create_engine
from constant import db_name, db_host, db_password, db_port, db_user

# STEP 1: EXTRACT
def fetch_open_food_facts_data(page_size=500):
    print("Fetching data from Open Food Facts API...")
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "json": 1,
        "page_size": page_size,
        "fields": "product_name,brands,countries,nutriments,categories,url",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['products']

# STEP 2: TRANSFORM
def transform_data(products):
    print("Transforming data...")
    df = pd.json_normalize(products)

    # Select relevant columns and rename
    df = df[[
        'product_name', 'brands', 'countries', 'categories',
        'nutriments.energy_100g', 'nutriments.fat_100g', 'nutriments.sugars_100g', 'url'
    ]]
    df.columns = [
        'product_name', 'brand', 'countries', 'categories',
        'energy_100g', 'fat_100g', 'sugars_100g', 'product_url'
    ]

    # Drop missing product names
    df = df.dropna(subset=['product_name'])

    # Fill NaNs with default values
    df = df.fillna({
        'brand': 'Unknown',
        'countries': 'Unknown',
        'categories': 'Uncategorized',
        'energy_100g': 0,
        'fat_100g': 0,
        'sugars_100g': 0,
        'product_url': ''
    })

    return df

# STEP 3: LOAD
def load_to_postgres(df, table_name='food_products'):
    print("Loading data into PostgreSQL...")

    engine = create_engine(
        f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require'
    )

    
    # Load to DB
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"{len(df)} records loaded to table `{table_name}` in database `{db_name}`")

# Main pipeline
def run_etl():
    products = fetch_open_food_facts_data()
    df = transform_data(products)
    load_to_postgres(df)

if __name__ == '__main__':
    run_etl()