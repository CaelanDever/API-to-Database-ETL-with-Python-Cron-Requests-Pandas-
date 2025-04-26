import requests
import pandas as pd
import psycopg2
from psycopg2 import sql

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
DB_SETTINGS = {
    'dbname': 'api_data_db',
    'user': 'api_user',
    'password': '------------',
    'host': 'localhost',
    'port': 5432
}

# Fetch data from API
response = requests.get(API_URL)
data = response.json()

# Transform data
price_usd = data['bitcoin']['usd']
timestamp = pd.Timestamp.now()

# Connect to database and insert
conn = psycopg2.connect(**DB_SETTINGS)
cur = conn.cursor()

# Ensure table exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS bitcoin_price (
        timestamp TIMESTAMPTZ PRIMARY KEY,
        price_usd FLOAT
    );
""")

# Insert data
cur.execute(sql.SQL("""
    INSERT INTO bitcoin_price (timestamp, price_usd)
    VALUES (%s, %s)
    ON CONFLICT (timestamp) DO NOTHING;
"""), [timestamp, price_usd])

conn.commit()
cur.close()
conn.close()

print(f"Inserted Bitcoin price {price_usd} USD at {timestamp}")
