import sqlite3
from datetime import datetime

def get_customer_count():
    query = """SELECT count, date FROM customer_count ORDER BY date DESC"""
    counts = []
    dates = []
    try:
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            counts.append(row[0])
            dates.append(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'))
        return counts, dates
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"error: {e}")
    finally:
        conn.close()
 

