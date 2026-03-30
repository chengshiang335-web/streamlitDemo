import os
import pymssql
import sys
import logging
import time


# 將上一層目錄加入系統路徑，以讀取 configLoader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configLoader.config_loader import load_db_config
 
# 設定 logging 基本配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


import logging
import pymssql


def get_conn(retry=8, delay=5, timeout=5):
    """
    建立 SQL Server 連線（含重試 + 喚醒檢查）
    """
    for attempt in range(1, retry + 1):
        try:
            logging.info(f"[DB] 嘗試連線 ({attempt}/{retry})")

            conn = pymssql.connect(
                server=os.getenv("DB_SERVER"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                login_timeout=timeout,
                timeout=timeout
            )

            # ✅ 驗證連線（避免假連線成功）
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            logging.info("[DB] 連線成功 ✅")
            return conn

        except pymssql.OperationalError as e:
            logging.error(f"[DB] 連線失敗 (attempt {attempt}): {e}")

        except Exception as e:
            logging.error(f"[DB] 未知錯誤: {e}", exc_info=True)

        # ⏳ 指數退避（避免狂打 DB）
        sleep_time = delay * attempt
        logging.info(f"[DB] 等待 {sleep_time} 秒後重試...")
        time.sleep(sleep_time)

    # ❌ 全部失敗
    raise Exception("[DB] 無法連線，已達最大重試次數")

def insert_to_db(history):
    import logging

    db_config = load_db_config()
    if not db_config:
        logging.error("錯誤: 無法載入資料庫設定")
        return

    table_name = db_config.get("table_name")
    connect = get_conn()

    if not connect:
        print("❌ 資料庫連線失敗")
        return

    try:
        cursor = connect.cursor()
        print("✅ 資料庫連線成功")

        df = history.reset_index()

        if df.empty:
            print("❌ 沒有股價資料")
            return

        # 先把所有 StockSymbol+Date 組合抓出來
        cursor.execute(f"SELECT StockSymbol, Date FROM {table_name}")
        existing = set(cursor.fetchall())  # {(symbol, date), ...}

        # 準備要寫入的資料
        records_to_insert = []

        for _, row in df.iterrows():
            stock_symbol = row['Symbol']
            date = row['Date'].date()
            company_name = row['Company']
            open_price = float(row['Open'])
            high = float(row['High'])
            low = float(row['Low'])
            close = float(row['Close'])
            volume = int(row['Volume'])

            # 🔍 檢查是否已存在 (PK: StockSymbol + Date)
            if (stock_symbol, date) in existing:
                print(f"⚠️ {stock_symbol} {date} 已存在，不寫入")
                continue

            records_to_insert.append((
                stock_symbol,
                company_name,
                date,
                open_price,
                high,
                low,
                close,
                volume
            ))

        # 批次寫入
        if records_to_insert:
            print(f"準備寫入 {len(records_to_insert)} 筆新資料...")
            INS_SQL = f"""
            INSERT INTO {table_name} (
                StockSymbol, [CompanyName], Date, 
                OpenPrice, DayHigh, DayLow, CurrentPrice, Volume
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(INS_SQL, records_to_insert)
            connect.commit()
            print(f"✅ 寫入完成，共 {len(records_to_insert)} 筆資料")
        else:
            print("⚠️ 沒有新資料需要寫入")

    except Exception as e:
        print("❌ 資料庫錯誤:", e)

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()
        print("🔚 連線關閉")