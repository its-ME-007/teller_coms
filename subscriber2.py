import paho.mqtt.client as mqtt
import json

broker = "localhost"
port = 1883  

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Subscriber2 Connected, Listening to message_to_2")
        client.subscribe("message_to_2")
    else:
        print("Bad connection, Returned code=", rc)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"[Subscriber2] Received: {payload}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "subscriber_2")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, keepalive=30)
    client.loop_forever()

if __name__ == "__main__":
    main()
