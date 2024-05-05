# 匯入連結資料庫模組
import psycopg2

# PostgreSQL連線資訊
DB_HOST = "salt.db.elephantsql.com"
DB_NAME = "midldwfg"
DB_USER = "midldwfg"
DB_PASSWORD = "p6RFJVuvTJ9mgqO6u7kO5Th8YET3BsR3"

# 建立資料庫連線
def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection