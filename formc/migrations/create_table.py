import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


def create_table():
    command = '''
        CREATE TABLE IF NOT EXISTS filings (
            id SERIAL PRIMARY KEY,
            cik VARCHAR(255) NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            street_address VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            zipcode VARCHAR(255),
            website VARCHAR(255),
            intermediary_name VARCHAR(255) NOT NULL,
            intermediary_cik VARCHAR(255),
            offering_type VARCHAR(255),
            offering_target VARCHAR(255),
            offering_maximum VARCHAR(255),
            offering_deadline VARCHAR(255),
            signature_name VARCHAR(255),
            signature_title VARCHAR(255),
            form_c_url VARCHAR(255),
            filing_date VARCHAR(255) NOT NULL
        );
    '''

    conn = None
    try:
        host=os.environ['DB_HOST']
        user=os.environ['DB_USER']
        password=os.environ['DB_PASS']
        dbname=os.environ['DB_NAME']
        conn = psycopg2.connect( host=host, user=user, password=password, dbname=dbname)
        cur = conn.cursor()

        cur.execute(command)
        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR: ', error)
    finally:
        if conn is not None:
            conn.close()


create_table()
