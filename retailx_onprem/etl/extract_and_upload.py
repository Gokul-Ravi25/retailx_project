import os
import pandas as pd
import oracledb
import boto3
from datetime import datetime

host = os.environ.get("ORACLE_HOST", "oracle-db")
port = int(os.environ.get("ORACLE_PORT", 1521))
service = os.environ.get("ORACLE_SERVICE", "FREEPDB1")
user = os.environ.get("ORACLE_USER", "system")
pwd = os.environ.get("ORACLE_PASSWORD")
table_name = 'CUSTOMERS'

s3_bucket = os.environ["S3_BUCKET"]
aws_region = os.environ.get("AWS_REGION", "ap-south-1")

s3 = boto3.client("s3", region_name=aws_region)

dsn = f"{host}:{port}/{service}"
con = oracledb.connect(user=user, password=pwd, dsn=dsn)
cur = con.cursor()

query = f"SELECT * FROM {table_name}"
cur.execute(query)

cols = [c[0] for c in cur.description]
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=cols)
con.close()

timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
local_path = f"/tmp/retailx_customers_{timestamp}.csv"
df.to_csv(local_path, index=False)

s3_key = f"bronze/customers/{os.path.basename(local_path)}"
s3.upload_file(local_path, s3_bucket, s3_key)

print(f"Upload successful: s3://{s3_bucket}/{s3_key}")
