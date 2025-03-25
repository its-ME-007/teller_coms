import paho.mqtt.client as mqtt
import json
import time

# MQTT Broker
broker = "localhost"
port = 1883  

# Updated available destinations to include users 1-10
users = {
    "1": "message_to_1",
    "2": "message_to_2",
    "3": "message_to_3",
    "4": "message_to_4",
    "5": "message_to_5",
    "6": "message_to_6",
    "7": "message_to_7",
    "8": "message_to_8",
    "9": "message_to_9",
    "10": "message_to_10"
}

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "publisher")
    client.connect(broker, port, keepalive=30)
    
    while True:
        print("\n===== MQTT Publisher =====")
        print("Select source:")
        for key in users:
            print(f"{key}. User {key}")
        
        source = input("Enter source number: ").strip()
        if source not in users:
            print("Invalid source. Try again.")
            continue
        
        print("\nSelect destination:")
        for key in users:
            if key != source:  # Prevent self-publishing
                print(f"{key}. User {key}")
        
        destination = input("Enter destination number: ").strip()
        if destination not in users or destination == source:
            print("Invalid destination. Try again.")
            continue
        
        message = input("Enter message: ").strip()
        payload_json = json.dumps({"source": f"User {source}", "message": message})
        
        # Publish actual message only to the selected destination topic
        client.publish(users[destination], payload_json)
        print(f"Published to {users[destination]}: {payload_json}")

        # Publish blank messages to all other topics
        empty_payload = json.dumps({})
        for key, topic in users.items():
            if key != destination:  # Send blank to all except the destination
                client.publish(topic, empty_payload)
                print(f"Sent blank message to {topic}")

        # Allow exit
        if input("Send another message? (y/n): ").strip().lower() != 'y':
            break
    
    client.disconnect()
    print("Publisher stopped.")

if __name__ == "__main__":
    main()