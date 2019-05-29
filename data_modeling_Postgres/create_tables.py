import psycopg2
from sql_queries import create_table_queries, drop_table_queries, create_FK_queries


def create_database():
    '''function: creates and connects to sparkifydb
    output: sparkifydb connection, cursor'''

    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    '''input: database connection, cursor
    function: drops tables defined in sql_queries'''

    for query in drop_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    '''input: database connection, cursor
    function: creates tables defined in sql_queries'''

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def create_FKs(cur, conn):
    '''input: database connection, cursor
    function: creates foreign keys between tables defined in sql_queries'''

    for query in create_FK_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''main function to open sparkify database connection,
    then drops and recreates tables and foreign keys defined in sql_queries'''

    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    create_FKs(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()