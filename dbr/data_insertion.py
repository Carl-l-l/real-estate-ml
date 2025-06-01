from databricks_handler import DatabricksHandler
import pandas as pd

if __name__ == "__main__":
    """
    This script is designed to create a table for the Real Estate dataset in Databricks and insert data from a CSV file into that table.
    It checks if the table already exists, and if not, it creates the table and inserts the data.
    """

    # Initialize handler
    db_handler = DatabricksHandler()
    
    # Create table
    target_table = {
        "catalog": "workspace",
        "schema": "default",
        "table_name": "real_estate_2",
    }

    real_estate_csv = pd.read_csv("data/Real estate.csv")
    target_table_columns = real_estate_csv.dtypes.apply(lambda x: 'decimal(10, 5)' if x == 'float64' else 'int').rename(lambda x: x.lower().replace(' ', '_').replace('-', '_'), axis='index').to_dict()
    print("Target Table Columns:", target_table_columns)
    
    target_table_exists = db_handler.table_exists(
        catalog=target_table["catalog"],
        schema=target_table["schema"],
        table_name=target_table["table_name"]
    )
    print(f"Target table exists: {target_table_exists}")

    if not target_table_exists:
        try:
            # Create table if it does not exist
            db_handler.create_table(
                catalog=target_table["catalog"],
                schema=target_table["schema"],
                table_name=target_table["table_name"],
                columns=target_table_columns,
                primary_key='no'
            )
            print(f"Table {target_table['table_name']} created successfully.")


            # Insert data from CSV into the table
            # db_handler.insert_data(
            #     catalog=target_table["catalog"],
            #     schema=target_table["schema"],
            #     table_name=target_table["table_name"],
            #     data_frame=real_estate_csv
            # )

            print(f"Data inserted into {target_table['table_name']} successfully.")
        except Exception as e:
            print(f"Error creating table or inserting data: {e}")

    # Close the connection
    db_handler.close()

