import psycopg2

# initialize postgres connection
def init_postgres_conn(host, port, database, user, password):
    try:
        conn = psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
