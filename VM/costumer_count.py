from datetime import datetime
import sqlite3
import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT script running!")

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

def get_data(client, userdata, message):
    print("Received message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload}")

    try:
        data = message.payload.decode('utf-8')
        print(f"Decoded Data: {data}")

        # Split the data string and get the last element
        elements = data.split()
        last_element = elements[-1]

        # Convert last element to integer and insert into the database
        count = int(last_element)
        insert_data(count)

    except UnicodeDecodeError as e:
        print(f"Failed to decode message payload: {e}")
    except ValueError as e:
        print(f"Failed to convert last element to integer: {e}")

# Subscribe to the topic "7c" and call get_data for each received message
subscribe.callback(get_data, "7c", hostname="74.235.100.12", userdata={"message_count": 0})
