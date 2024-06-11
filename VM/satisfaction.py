from datetime import datetime
import sqlite3
import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT script running!")

def create_table():
    try:
        query = """CREATE TABLE IF NOT EXISTS satisfaction(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    satisfaction INTEGER NOT NULL, 
                    date TEXT NOT NULL)"""
        conn = sqlite3.connect("aktionshus.db")
        cur = conn.cursor()
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

def get_data(client, userdata, message):
    print("Received message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload}")

    try:
        data = message.payload.decode('utf-8')
        print(f"Decoded Data: {data}")

        elements = data.split()
        second_element = elements[1].strip("'") 

        satisfaction = int(second_element)
        insert_data(satisfaction)

    except UnicodeDecodeError as e:
        print(f"Failed to decode message payload: {e}")
    except ValueError as e:
        print(f"Failed to convert second element to integer: {e}")

subscribe.callback(get_data, "7c", hostname="74.235.100.12", userdata={"message_count": 0})
