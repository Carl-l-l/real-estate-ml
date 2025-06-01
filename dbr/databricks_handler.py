from databricks import sql
import pandas as pd
from dotenv import load_dotenv
import os

class DatabricksHandler:
    """ A class to handle all interactions with Databricks SQL """
    def __init__(self):
        """ Initialize the Databricks connection using environment variables """

        load_dotenv() # Ensure loading of environment variables
        self.connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_ACCESS_TOKEN"),
        )
        self.cursor = self.connection.cursor()


    def create_table(self, catalog, schema, table_name, columns: dict, primary_key=None):
        """ Create a table in the specified catalog and schema with the given columns """
        sql_create = f"""
            CREATE TABLE IF NOT EXISTS {catalog}.{schema}.{table_name} (
                {', '.join([f"{col} {dtype}" for col, dtype in columns.items()])}

                --- Set primary key if specified
                {', PRIMARY KEY (' + primary_key + ')' if primary_key else ''}
            )
        """
        self.cursor.execute(sql_create)
        print(f"Table {table_name} created successfully in {catalog}.{schema}.")


    def table_exists(self, catalog, schema, table_name) -> bool:
        """ Check if a table exists in the specified catalog and schema """
        query = f"""
            SELECT table_catalog, table_schema, table_name
            FROM system.information_schema.tables
            WHERE table_catalog = '{catalog}'
              AND table_schema = '{schema}'
              AND table_name = '{table_name}'
        """
        result = self.cursor.execute(query).fetchall()
        exists = len(result) > 0
        return exists
    

    def insert_data(self, catalog, schema, table_name, data_frame: pd.DataFrame):
        """ Insert data from a pandas DataFrame into the specified table """
        for index, row in data_frame.iterrows():
            insert_sql = f"""
                INSERT INTO {catalog}.{schema}.{table_name} 
                VALUES ({', '.join([str(value) if pd.notna(value) else 'NULL' for value in row])});
            """
            # print(f"Executing insert for row {index + 1}: {insert_sql}")
            self.cursor.execute(insert_sql)
        print(f"Data inserted into {table_name} successfully in {catalog}.{schema}.")


    def close(self):
        """ Close connection to Databricks """
        self.cursor.close()
        self.connection.close()
        print("Connection closed.")

    


