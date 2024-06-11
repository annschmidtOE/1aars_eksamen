import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT script running!")

def get_data(client, userdata, message):
    print("Received message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload}")

    try:
        data = message.payload.decode('utf-8')  
        print(f"Decoded Data: {data}")
    except UnicodeDecodeError as e:
        print(f"Failed to decode message payload: {e}")

subscribe.callback(get_data, "7c", hostname="74.235.100.12", userdata={"message_count": 0})
