from io import BytesIO
import pandas as pd
import cryptography_handler

access_key_encrypted = b'gAAAAABnFhGuEZIpwBMDZs5u-3G-ccqLh_H37-7exik8uCQD0FBNJ6iiDb2Ocs3dy5eakINcC-DqHQnNv-ijrOHLhu1EofTgWDYsIdf1sr3YIJl4V0qImnc='
secret_key_encrypted = b'gAAAAABnFhHE1eDnu8aU9-nEVwxIGKC7XtV-XJA9_CSpb6ABvocfwrMYcsg2BIhsxH67ev_yzlQ6DmalNe06YxJQGG8gWA-2hTaLShRyGHxhrVBI2LzdInNKSFK_sqOs2CDI3nC7wgpC'

key = cryptography_handler.load_key()

def return_pandas_df_from_csv(csv_path):
    # Read CSV with pandas directly from S3
    df = pd.read_csv(
        csv_path,
        #  nrows=10,
        storage_options={
            'key': cryptography_handler.decrypt_api_key(access_key_encrypted,key),
            'secret': cryptography_handler.decrypt_api_key(secret_key_encrypted,key),
            'client_kwargs': {'region_name': 'us-east-2'}
        }
    )
    return df

def convert_list_to_df(dict_list):
    return pd.DataFrame(dict_list)

def return_df_as_table_data(df):
    # Extract table names, columns, and sample data
    table_data = []
    for index, row in df.iterrows():
        table_name = row['table_name']
        columns = eval(row['columns'])  # Convert string representation of list to actual list
        sample_data = row['sample_data']
        table_data.append({'table_name': table_name, 'columns': columns, 'sample_data': sample_data})
    return table_data



def return_create_statement_from_df(dataframe, schema_name, table_name):
    create_table_statement = None
    try:
        type_mapping = {
            'int64': 'BIGINT',
            'float64': 'FLOAT',
            'datetime64[ns]': 'TIMESTAMP',
            'bool': 'BOOLEAN',
            'object': 'TEXT'
        }
        fields = []
        for column, dtype in dataframe.dtypes.items():
            # If the column name contains 'date', we should assign it a TIMESTAMP type
            if 'date' in column.lower() and not 'id' in column.lower():
                sql_type = 'TEXT'
            else:
                sql_type = type_mapping.get(str(dtype), 'TEXT')
            fields.append(f"{column} {sql_type}")
        
        create_table_statement = f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (\n"
        create_table_statement += ",\n".join(fields)
        create_table_statement += "\n);"
    except Exception as e:
        print(str(e))
    finally:
        return create_table_statement
    

def return_truncate_statement(schema_name, table_name):
    try:
        query = f"""
        DO $$
            BEGIN
            IF EXISTS (SELECT FROM pg_tables WHERE schemaname = '{schema_name}' AND tablename  = '{table_name}') THEN
                 TRUNCATE TABLE {schema_name}.{table_name};
            END IF;
            END
        $$;
        """
    except Exception as e:
        print(str(e))
    finally:
        return query
    

def return_insert_statement_from_df(dataframe, schema_name, table_name):
    insert_statement = None
    print(table_name)
    try:
        columns = ', '.join([f'"{col.lower()}"' for col in dataframe.columns])  # Quote column names
        values_list = []
        for _, row in dataframe.iterrows():
            value_strs = []
            for val in row.values:
                if pd.isna(val):
                    value_strs.append("NULL")
                elif isinstance(val, str):
                    val = val.replace("'", "''")  # Escape single quotes
                    value_strs.append(f"'{val}'")
                elif isinstance(val, pd.Timestamp):
                    timestamp_str = val.strftime('%Y-%m-%d %H:%M:%S')
                    value_strs.append(f"'{timestamp_str}'")  # Ensure timestamp is quoted
                elif isinstance(val, (int, float)):
                    value_strs.append(str(val))  # Directly append numeric values without quotes
                else:
                    value_strs.append(f"'{val}'")

            values_list.append(f"({', '.join(value_strs)})")

        values = ', '.join(values_list)
        insert_statement = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES {values};"
    except Exception as e:
        print(f"{schema_name} {table_name} Error occurred: {str(e)}")
    finally:
        return insert_statement

