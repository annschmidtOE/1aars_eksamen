from datetime import datetime
import sqlite3

def create_table():
    try:
        query = """CREATE TABLE IF NOT EXISTS costumer_count(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    count INTEGER NOT NULL, 
                    date TEXT NOT NULL)"""
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"error: {e}")
    finally:
        conn.close()

def insert_data(count):
    try:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        data = (count, formatted_datetime)
        
        query = """INSERT INTO costumer_count(count, date) VALUES (?, ?)"""
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"error: {e}")
    finally:
        conn.close()

create_table()

count = 0

for i in range(10): 
    count += 1
    insert_data(count)
