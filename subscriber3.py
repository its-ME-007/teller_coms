import paho.mqtt.client as mqtt
import json
import time
import threading

# Define the MQTT broker address and port
broker = "localhost"
port = 1883  # Default MQTT port

# Check if we're using MQTT Client V2 API
try:
    mqtt.CallbackAPIVersion.VERSION2
    using_v2 = True
except AttributeError:
    using_v2 = False

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected OK, Returned code=", rc)
        client.connected_flag = True  # Flag to indicate success
        topics = [("message_from_2", 0), ("message_from_3", 0), ("message_from_1", 0)]
        client.subscribe(topics)  # Ensure resubscription on reconnect
    else:
        print("Bad connection, Returned code=", rc)
        client.bad_connection_flag = True

# Define on_disconnect with compatible signatures for both v1 and v2
def on_disconnect(client, userdata, rc, *args):
    print(f"Disconnected with result code {rc}")
    if rc != 0:
        print("Unexpected disconnection. Attempting to reconnect...")

# Subscriber callback function
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"Error decoding JSON for topic {topic}: {payload}")
        return
    print(f"Received message on {topic}: {data}")

def main():
    # Create a single client for both publishing and subscribing
    if using_v2:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "user_3")
    else:
        client = mqtt.Client("user_1")
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Set up will message
    client.will_set("user_status", payload=json.dumps({"status": "offline", "user": "user_3"}), qos=1, retain=True)
    
    # Connect to the broker
    client.connect(broker, port, keepalive=30)
    
    # Start the network loop in a background thread
    client.loop_start()
    
    while True:
        try:
            print("Enter message to be published. Ctrl+C to exit:")
            message = input()
            payload_json = json.dumps({"value": message})
            client.publish("message_from_3", payload_json)
            print(f"Published from user3: {payload_json}")
        except KeyboardInterrupt:
            print("Exiting application...")
            client.loop_stop()
            client.disconnect()
            break

if __name__ == "__main__":
    main()