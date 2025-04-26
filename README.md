API to Database ETL with Python (Cron, Requests, Pandas)
-
⚡️ 30 Second Summary
-
Modern businesses rely on timely data from external sources to fuel analytics and decision-making. In this hands-on project, I built a simple yet powerful ETL (Extract, Transform, Load) pipeline using Python to fetch data from a public API and insert it into a PostgreSQL database. The script is scheduled with cron on a Red Hat Enterprise Linux (RHEL) server, enabling full automation.

This type of automation is widely used by Data Engineers, DevOps Engineers, and System Administrators who support real-time and batch data workflows.

🚀 Key Skills Learned:
-
🛠️ Python scripting for automation

🌐 API data extraction using requests

📊 Data transformation with pandas

🗄️ PostgreSQL data loading using psycopg2

⏰ Linux cron scheduling for periodic jobs

📋 Logging & monitoring for operational reliability

🧩 Where This Fits
-
This project forms a foundational step in data pipeline development. It’s a key building block in architectures ranging from simple local ETLs to cloud-based pipelines using services like AWS Lambda, Airflow, or Glue. It teaches core concepts that can scale into enterprise-grade workflows.

🧱 Project Structure
-
api_to_db_etl/
├── fetch_bitcoin_price.py     # Python script that performs the ETL
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── setup_instructions.md      # Setup and cron configuration steps

📐 Format Requirements
-
Use Python 3

Use PostgreSQL as the target database

Compatible with Red Hat Enterprise Linux

Cron-based scheduling (every hour)

Ensure good error handling (no log file location assumption)

🔧 Technical Elements
-
Languages & Tools

Python

Requests

Pandas

Psycopg2

PostgreSQL

Crontab (RHEL Linux)

📘 Project Details
-
🏷️ Title: API to Database ETL with Python
-
🧠 Overview
-
This project demonstrates how to build and automate a simple data pipeline:

Extract real-time Bitcoin prices from the CoinGecko API.

Transform the JSON response into a structured format.

Load it into a PostgreSQL database.

Automate it with a scheduled cron job.

🖼️ Screenshot Gallery
-
📌 Screenshot Placeholder: Successful script output in terminal

<img width="379" alt="bitcoin" src="https://github.com/user-attachments/assets/bb6f44c9-0f19-489a-8e87-88445cbff40e" />

📌 Screenshot Placeholder: Cron job entry in crontab -l

<img width="452" alt="cron" src="https://github.com/user-attachments/assets/a75947c4-f489-43ad-a6d3-e2101ccd567d" />

📌 Screenshot Placeholder: Query result in PostgreSQL CLI showing inserted data

<img width="449" alt="sql" src="https://github.com/user-attachments/assets/ddea1fdc-dc7b-426f-a204-4398d6eb8590" />

🧱 Detailed Project Sections
-
1. Environment Setup

Install Python:

sudo yum install python3 -y

Install dependencies:

pip3 install requests pandas psycopg2-binary

Install and start PostgreSQL:

sudo yum install postgresql-server -y
sudo postgresql-setup --initdb
sudo systemctl start postgresql

Create database and user:

sudo -u postgres createdb api_data_db
sudo -u postgres createuser api_user -P

Grant privileges:

GRANT ALL PRIVILEGES ON DATABASE api_data_db TO api_user;

📌 Screenshot Placeholder: Database and user creation steps

<img width="420" alt="dbe" src="https://github.com/user-attachments/assets/f94b6e5c-3157-4e37-aa49-bde2571c9b2b" />

2. Python ETL Script

import requests
import pandas as pd
import psycopg2
from psycopg2 import sql

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
DB_SETTINGS = {
    'dbname': 'api_data_db',
    'user': 'api_user',
    'password': 'your_db_password',
    'host': 'localhost',
    'port': 5432
}

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    price_usd = data['bitcoin']['usd']
    timestamp = pd.Timestamp.now()

    conn = psycopg2.connect(**DB_SETTINGS)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bitcoin_price (
            timestamp TIMESTAMPTZ PRIMARY KEY,
            price_usd FLOAT
        );
    """)

    cur.execute(sql.SQL("""
        INSERT INTO bitcoin_price (timestamp, price_usd)
        VALUES (%s, %s)
        ON CONFLICT (timestamp) DO NOTHING;
    """), [timestamp, price_usd])

    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted Bitcoin price {price_usd} USD at {timestamp}")

except Exception as e:
    print(f"An error occurred: {e}")

📌 Screenshot Placeholder: Script terminal output and sample database row

<img width="379" alt="bitcoin" src="https://github.com/user-attachments/assets/c749b772-b779-48e7-b704-7469ce600370" />

3. Testing

Run script:

python3 fetch_bitcoin_price.py

Verify data:

sudo -u postgres psql -d api_data_db -c "SELECT * FROM bitcoin_price;"

📌 Screenshot Placeholder: Database query showing inserted row

<img width="449" alt="sql" src="https://github.com/user-attachments/assets/cb17893d-7d1d-42bc-a0ea-1db7940ff6fc" />

4. Cron Setup

Edit crontab:

crontab -e

Add entry:

0 * * * * /usr/bin/python3 /home/youruser/fetch_bitcoin_price.py >> /home/youruser/fetch_bitcoin_price.log 2>&1

📌 Screenshot Placeholder: Crontab entry confirmation

<img width="452" alt="cron" src="https://github.com/user-attachments/assets/ab1c35f6-0d84-47c9-a0e1-e5093967dc10" />

5. Monitoring

Monitor log file if created:

tail -f /home/youruser/fetch_bitcoin_price.log

📌 Screenshot Placeholder: Error log sample (if any)

<img width="451" alt="logz" src="https://github.com/user-attachments/assets/a7df6546-7ad0-488a-aa82-50531237b8a3" />

🧠 Challenges & Solutions
-
Hardcoding credentials ➡ Used plaintext (for demo), should be stored in environment variables.

Cron script path issues ➡ Used full path to Python and script to avoid $PATH issues.

Data duplication ➡ Handled via ON CONFLICT DO NOTHING for primary key.

Missing log file ➡ Updated cron job to use user home directory for log output.

🏁 Summary
-
🎉 Congratulations, you've completed the project!

In this project, you:

Installed Python and PostgreSQL on RHEL

Created a database and user

Wrote a Python script to extract API data and load it into a DB

Scheduled the script using cron

Verified, monitored, and logged the job output

These are foundational skills for any backend developer, data engineer, or DevOps role.

🧹 Cleanup Steps
-
Remove cron job:

crontab -e   # and delete the line

Drop the database:

sudo -u postgres dropdb api_data_db

Delete user:

sudo -u postgres dropuser api_user

Remove log:

rm /home/youruser/fetch_bitcoin_price.log

📚 References
-

CoinGecko API Documentation

Psycopg2 Docs

Pandas Documentation

Requests Documentation

PostgreSQL Manual

Crontab Guru – for cron expression help

💡 Tip: Keep this project in a GitHub repo to showcase your skills to employers. Include this README.md and sample logs/data files to demonstrate your understanding of ETL, automation, and Linux scripting.
