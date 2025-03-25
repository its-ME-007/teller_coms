import paho.mqtt.client as mqtt
import json
import threading

class MQTTSubscriber:
    def __init__(self, broker="localhost", port=1883, client_id=None):
        """
        Initialize MQTT Subscriber
        
        :param broker: MQTT broker address
        :param port: MQTT broker port
        :param client_id: Unique client identifier
        """
        # Use a default client ID if not provided
        if client_id is None:
            client_id = f"subscriber_{threading.get_ident()}"
        
        self.broker = broker
        self.port = port
        self.client_id = client_id
        
        # Create MQTT client with the latest callback API version
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
        
        # Set up callback methods
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        # Logging flag to prevent multiple connection logs
        self._first_connection = True
    
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        """
        Connection callback method
        
        :param rc: Return code of connection
        """
        if rc == 0:
            if self._first_connection:
                print(f"[{self.client_id}] Connected successfully")
                # Subscribe to a topic specific to this subscriber
                topic = f"message_to_{self.client_id.split('_')[-1]}"
                self.client.subscribe(topic)
                self._first_connection = False
        else:
            print(f"[{self.client_id}] Bad connection. Returned code: {rc}")
    
    def _on_message(self, client, userdata, message):
        """
        Message received callback method
        
        :param message: Received MQTT message
        """
        try:
            payload = message.payload.decode("utf-8")
            print(f"[{self.client_id}] Received on {message.topic}: {payload}")
            
            # Optional: Parse JSON if needed
            if payload:
                try:
                    parsed_payload = json.loads(payload)
                    print(f"Parsed Message: {parsed_payload}")
                except json.JSONDecodeError:
                    print("Could not parse message as JSON")
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def connect(self, keepalive=30):
        """
        Connect to the MQTT broker
        
        :param keepalive: Connection keepalive interval
        """
        try:
            self.client.connect(self.broker, self.port, keepalive)
            print(f"[{self.client_id}] Connecting to {self.broker}:{self.port}")
        except Exception as e:
            print(f"[{self.client_id}] Connection error: {e}")
    
    def start(self):
        """
        Start the MQTT client loop
        """
        # Use loop_start for non-blocking operation
        self.client.loop_start()
    
    def stop(self):
        """
        Stop the MQTT client loop
        """
        self.client.loop_stop()

def create_subscribers(count=10):
    """
    Create multiple MQTT subscribers
    
    :param count: Number of subscribers to create
    """
    subscribers = []
    
    for i in range(1, count + 1):
        subscriber = MQTTSubscriber(client_id=f"subscriber_{i}")
        subscriber.connect()
        subscriber.start()
        subscribers.append(subscriber)
    
    return subscribers

def main():
    """
    Main function to run multiple subscribers
    """
    subscribers = create_subscribers()
    
    # Keep the main thread running
    try:
        # Use loop to keep program running
        while True:
            input("Press Enter to quit...\n")
            break
    except KeyboardInterrupt:
        print("\nStopping subscribers...")
    finally:
        for subscriber in subscribers:
            subscriber.stop()

if __name__ == "__main__":
    main()