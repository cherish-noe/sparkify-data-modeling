import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to sparkifydb
    - Return the connection and cursor to sparkifydb
    """

    # establish the connection and connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=myatnoe")
    conn.set_session(autocommit=True)

    # create a cursor object using the cursor() method
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=myatnoe")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in 'drop_table_queries' lists
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in 'create_table_queries' lists
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database
    
    - Establishes connection with the sparkify database and get cursor to it

    - Drops all the tables

    - Create all tables needed

    - Finally, close the connection
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()