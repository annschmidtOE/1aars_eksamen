from datetime import datetime
import sqlite3

def create_table():
    try:
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
        
        cur.execute("DROP TABLE IF EXISTS satisfaction")
        
        query = """CREATE TABLE IF NOT EXISTS satisfaction(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    satisfaction INTEGER NOT NULL, 
                    date TEXT NOT NULL)"""
        
        cur.execute(query)
        conn.commit()
        print("Table created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"error: {e}")
    finally:
        conn.close()

def insert_data(satisfaction):
    try:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        data = (satisfaction, formatted_datetime)

        query = """INSERT INTO satisfaction(satisfaction, date) VALUES (?, ?)"""
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        print(f"Data inserted successfully: {data}")
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"error: {e}")
    finally:
        conn.close()

create_table()

while True:
    try:
        satisfaction = int(input("Enter 3 for perfect, 2 for fine, and 1 for horrible (or any other number to quit): "))
        if satisfaction in [1, 2, 3]:
            print(f"Inserting data: satisfaction={satisfaction}")
            insert_data(satisfaction)
        else:
            print("Exiting...")
            break
    except ValueError:
        print("Invalid input. Please enter a number.")
