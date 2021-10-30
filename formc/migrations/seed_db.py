import psycopg2
from psycopg2.extras import Json
import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

table_name = 'filings'

# --------------
# HANDLE SEED 1
# --------------

# use Python's open() function to load the JSON data
with open('all_formc_2019_to_2021.json') as json_data:

    # use load() rather than loads() for JSON files
    seed1 = json.load(json_data)

# concatenate a SQL string
sql_string = 'INSERT INTO {} '.format( table_name )

# if record list then get column names from first key
if type(seed1) == list:
    first_record = seed1[0]

    columns = list(first_record.keys())
else:
    print ("Needs to be an array of JSON objects")
    sys.exit()

# enclose the column names within parenthesis
sql_string += "(" + ', '.join(columns) + ")\nVALUES "

# enumerate over the record
for i, record_dict in enumerate(seed1):

    # iterate over the values of each record dict object
    values = []
    for col_names, val in record_dict.items():

        # Postgres strings must be enclosed with single quotes
        if type(val) == str:
            # escape apostrophies with two single quotations
            val = val.replace("'", "''")
            val = "'" + val + "'"
        elif val == None:
            val = 'NULL'

        values += [ str(val) ]

    # join the list of values and enclose record in parenthesis
    sql_string += "(" + ', '.join(values) + "),\n"

# --------------
# HANDLE SEED 2
# --------------

# use Python's open() function to load the JSON data
with open('all_formc_through_2019.json') as json_data:

    # use load() rather than loads() for JSON files
    seed2 = json.load(json_data)

# enumerate over the record
for i, record_dict in enumerate(seed2):

    # iterate over the values of each record dict object
    values = []
    for col_names, val in record_dict.items():

        # Postgres strings must be enclosed with single quotes
        if type(val) == str:
            # escape apostrophies with two single quotations
            val = val.replace("'", "''")
            val = "'" + val + "'"
        elif val == None:
            val = 'NULL'

        values += [ str(val) ]

    # join the list of values and enclose record in parenthesis
    sql_string += "(" + ', '.join(values) + "),\n"

# remove the last comma and end statement with a semicolon
sql_string = sql_string[:-2] + ";"


def seed_db():
    command = sql_string

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


seed_db()
