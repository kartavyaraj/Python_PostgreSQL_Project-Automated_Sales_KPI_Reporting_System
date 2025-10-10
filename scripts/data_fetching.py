import pandas as pd
from sqlalchemy import create_engine # type: ignore 

# ------------------------ DATABASE CREDENTIALS ------------------------
db_user = "Username"
db_password = "Password"
db_host = "Host(by default: localhost)"
db_name = "Database Name"

# ------------------------ CREATING ENGINE ------------------------
def get_engine():
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}")
    return engine

# ------------------------ JOINING TABLES ------------------------
def fetch_merged_data(engine):
    merged_df = pd.read_sql("""
    SELECT t.transactionid, t.trans_date, t.quantity, t.discount, t.paymentmethod,
        c.name AS customer_name, c.city AS customer_city, c.gender,
        p.productname, p.category, p.subcategory, p.unitprice, p.costprice,
        s.storename, s.city AS store_city, s.region
    FROM transactions t
    LEFT JOIN customers c ON t.customerid = c.customerid
    LEFT JOIN products p ON t.productid = p.productid
    LEFT JOIN stores s ON t.storeid = s.storeid
    """, engine)
    return merged_df

# ------------------------ DATA VALIDATION ------------------------
def data_validation(merged_df):
    null_columns = merged_df.columns[merged_df.isnull().any()].tolist()
    if null_columns:
        raise ValueError(f"Null values found in columns: {null_columns}")

    duplicate_count = merged_df.duplicated().sum()
    if duplicate_count > 0:
        raise ValueError(f"Duplicate rows found: {duplicate_count}")