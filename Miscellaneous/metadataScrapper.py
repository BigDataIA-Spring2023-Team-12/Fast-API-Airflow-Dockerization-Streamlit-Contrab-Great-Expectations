import boto3
import json
import sqlite3


def get_file_structure(bucket_name, prefixes, depth=3):
    """
    Recursively gets the file structure of an S3 bucket up to the specified depth.
    """
    s3 = boto3.client('s3')
    files = []

    def get_files(prefix, level):
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
        if 'Contents' in response:
            files.extend([{'Key': obj['Key'], 'Size': obj['Size']} for obj in response['Contents']])
        if 'CommonPrefixes' in response and level < depth:
            for common_prefix in response['CommonPrefixes']:
                get_files(common_prefix['Prefix'], level + 1)

    for prefix in prefixes:
        get_files(prefix, 1)

    return files


def store_file_structure(bucket_name, prefixes, json_file_path, db_file_path, table_name):
    # Get the file structure of the S3 bucket up to level 3
    files = get_file_structure(bucket_name, prefixes, depth=3)

    # Store the file structure in a JSON file
    with open(json_file_path, 'w') as f:
        json.dump(files, f)

    # Create a SQLite database and table to store the file structure
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 key TEXT,
                 size INTEGER)''')

    # Insert the file structure into the SQLite database
    for file in files:
        c.execute(f"INSERT INTO {table_name} (key, size) VALUES (?, ?)", (file['Key'], file['Size']))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


def main():
    bucket_name_goes = 'noaa-goes18'
    bucket_name_nexrad = 'noaa-nexrad-level2'
    prefixes_goes = ['ABI-L1b-RadC/2022/', 'ABI-L1b-RadC/2022/']
    prefixes_nexrad = ['2022/', '2023/']
    json_file_path_goes = 'geos.json'
    json_file_path_nexrad = 'nexrad.json'
    db_file_path = 'metadata.db'
    table_name_goes = 'GEOS'
    table_name_nexrad = 'Nexrad'

    store_file_structure(bucket_name_goes, prefixes_goes, json_file_path_goes, db_file_path, table_name_goes)
    store_file_structure(bucket_name_nexrad, prefixes_nexrad, json_file_path_nexrad, db_file_path, table_name_nexrad)


if __name__ == '__main__':
    main()
