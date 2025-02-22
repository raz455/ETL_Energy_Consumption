from extract import extract_data
from transform import transform_data
import psycopg2
import argparse

def load_data(file_path, database, host, user, password, port):
    connection = psycopg2.connect(
        database=database,
        host=host,
        user=user,
        password=password,
        port=port
    )

    cursor = connection.cursor()

    print("Loading data...")
    data = extract_data(file_path)

    print("Transforming data...")
    data_transform = transform_data(data)

    column_name = data_transform.columns[-1]

    # Create table
    query_create_table = f"""
    CREATE TABLE IF NOT EXISTS {column_name} (
        ID SERIAL PRIMARY KEY,
        continent VARCHAR(50) NOT NULL,
        country VARCHAR(50) NOT NULL,
        {column_name} DECIMAL
    );
    """
    cursor.execute(query_create_table)

    # Start loading data
    print("Inserting data...")
    for _, row in data_transform.iterrows():
        query_insert_value = f"""
        INSERT INTO {column_name} (continent, country, {column_name})
        VALUES ('{row[0]}', '{row[1]}', {row[2]});
        """
        cursor.execute(query_insert_value)

    connection.commit()
    cursor.close()
    connection.close()

    print("ETL process completed successfully.\n")
    return "All processes completed."

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional arguments
    parser.add_argument("-f", "--file", required=True, help="File path of your dataset")
    parser.add_argument("-db", "--database", required=True, help="Database name")
    parser.add_argument("-hs", "--host", required=True, help="Your PostgreSQL host")
    parser.add_argument("-u", "--user", required=True, help="PostgreSQL username")
    parser.add_argument("-pass", "--password", required=True, help="PostgreSQL password")
    parser.add_argument("-p", "--port", required=True, help="PostgreSQL port")
    
    # Read arguments from command line
    args = parser.parse_args()

    load_data(args.file, args.database, args.host, args.user, args.password, args.port)
