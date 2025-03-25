# RVCE Department Project - Teller loop

## MQTT Communication System

A simple MQTT-based messaging system that demonstrates publisher-subscriber pattern communication between multiple clients.

### Overview

This project provides a lightweight implementation of a messaging system using the MQTT protocol. It includes:

- A central publisher for sending messages
- Multiple subscriber clients that listen for messages
- A manager script to handle starting and stopping subscribers

The system allows messages to be sent from one user to another while maintaining privacy by only delivering the actual message content to the intended recipient (other subscribers receive empty messages).

### Requirements

- Python 3.9+
- paho-mqtt library

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mqtt-messaging-system.git
   cd mqtt-messaging-system
   ```

2. Install the required dependencies:
   ```
   pip install paho-mqtt
   ```

3. Make sure you have an MQTT broker running. This project is configured to use a local broker:
   - For local testing, you can install Mosquitto:
     - On Ubuntu: `sudo apt install mosquitto mosquitto-clients`
     - On macOS: `brew install mosquitto`
     - On Windows: Download from [Eclipse Mosquitto](https://mosquitto.org/download/)

### Project Structure

- `main.py` - Manager script to start and stop all subscribers
- `publisher.py` - Client for sending messages to specific subscribers
- `subscriber1.py`, `subscriber2.py`, `subscriber3.py` - Subscriber clients that listen for messages

### Usage

#### Starting the System

1. Start your MQTT broker (if not already running):
   ```
   mosquitto
   ```

2. Run the OOPS subscriber script to start all subscribers:
   ```
   python sub_oops.py
   ```

3. In a separate terminal, run the publisher script:
   ```
   python pub_update.py
   ```

#### Sending Messages

When running the publisher:

1. Select a source user (1-10)
2. Select a destination user (1-10)
3. Enter your message
4. Choose whether to send another message or exit

#### Stopping the System

- Press `Ctrl+C` in the terminal running `main.py` to gracefully stop all subscribers.

### How It Works

1. The `main.py` script spawns and manages the three subscriber processes.
2. Each subscriber connects to the MQTT broker and subscribes to its specific topic (e.g., `message_to_1`).
3. The publisher allows a user to:
   - Select which user they want to send a message as
   - Select which user they want to send a message to
   - Type the message content
4. When a message is sent:
   - The actual message with content is sent to the intended recipient's topic
   - Empty messages are sent to all other topics to maintain privacy

### Extending the System

- Add more subscribers by:
  1. Creating new subscriber files
  2. Adding them to the `subscribers` list in `main.py`
  3. Adding corresponding topics in `publisher.py`

