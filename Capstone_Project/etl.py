import configparser
import psycopg2
from sqlqueries import create_table_queries, drop_table_queries,  copy_table_queries, insert_table_queries


def drop_tables(cur, conn):
    '''This function drops all tables on Redshift'''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    '''This function creates stagaing tables and the fact and dimension tables on Redshift'''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
def load_staging_tables(cur, conn):
    ''' This function loads data from S3 into staging tables on Redshift'''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    ''' This function transforms data from staging tables into fact and dimension tables on Redshift'''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()