# import boto3
# import boto3
# import zipfile
# import os
# import dask.dataframe as dd
# from io import BytesIO


# access_key_encrypted = ""
# secret_key_encrypted = ""

# source_bucket_name = "lenora.health-data.set"
# source_zip_key = "SyH-DR_CSV_Data.zip"
# target_bucket_name = "processed.lenora.dataset"

# # Create S3 client
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=access_key_encrypted,
#     aws_secret_access_key=secret_key_encrypted,
#     region_name='us-east-2'
# )


# def download_zip_and_load_to_destination_bucket():
#         # Step 1: Download the ZIP file from the source S3 bucket
#     zip_obj = s3_client.get_object(Bucket=source_bucket_name, Key=source_zip_key)
#     buffer = BytesIO(zip_obj['Body'].read())

#     # Step 2: Extract the CSV files from the ZIP archive
#     with zipfile.ZipFile(buffer, 'r') as zip_ref:
#         csv_filenames = [name for name in zip_ref.namelist() if name.endswith('.csv')]
        
#         for csv_filename in csv_filenames:
#             # Read CSV file
#             with zip_ref.open(csv_filename) as csv_file:
#                 # Step 3: Upload the extracted CSV files to the target S3 bucket
#                 s3_client.upload_fileobj(
#                     Fileobj=csv_file,
#                     Bucket=target_bucket_name,
#                     Key=os.path.basename(csv_filename)
#                 )

#     return csv_filenames

# def return_csv_files(csv_filenames):
#     s3_csv_paths = [f's3://{target_bucket_name}/{os.path.basename(csv_filename)}' for csv_filename in csv_filenames]
#     return s3_csv_paths

# def upload_csv_to_s3(file_name):
#     # Default the target file name if not specified
#     target_file_name = os.path.basename(file_name)
#     # Upload the file
#     with open(file_name, 'rb') as file_obj:
#         s3_client.upload_fileobj(
#             Fileobj=file_obj,
#             Bucket=target_bucket_name,
#             Key=target_file_name
#         )
#     print(f"File {file_name} uploaded to s3://{target_bucket_name}/{target_file_name}")
