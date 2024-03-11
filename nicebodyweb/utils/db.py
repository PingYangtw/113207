# 匯入連結資料庫模組
import psycopg2

# PostgreSQL連線資訊
DB_HOST = "berry.db.elephantsql.com"
DB_NAME = "elnxzanb"
DB_USER = "elnxzanb"
DB_PASSWORD = "SAMzkYmrmen23l2a42UZIVPJsO8w41XM"

# 建立資料庫連線
def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection