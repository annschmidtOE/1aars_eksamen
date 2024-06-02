import sqlite3
from datetime import datetime

def get_satisfaction_count():
    query = """SELECT satisfaction, date FROM satisfaction ORDER BY date DESC"""
    satisfaction = []
    dates = []
    try:
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[0] in [1, 2, 3]:
                satisfaction.append(row[0])
            else:
                print(f"Unexpected satisfaction value: {row[0]}")
            
            date_str = row[1]
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                dates.append(date_obj)
            except ValueError:
                print(f"Error parsing date: {date_str}")
                continue
            
        return satisfaction, dates
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"error: {e}")
    finally:
        if conn:
            conn.close()
