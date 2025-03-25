import subprocess
import time
import signal
import sys

# Updated list of subscriber scripts to include subscribers 4-10
subscribers = [
    "subscriber1.py", "subscriber2.py", "subscriber3.py", 
    "subscriber4.py", "subscriber5.py", "subscriber6.py", 
    "subscriber7.py", "subscriber8.py", "subscriber9.py", 
    "subscriber10.py"
]

# Store processes
processes = []

def start_subscribers():
    for script in subscribers:
        print(f" Starting {script}...")
        process = subprocess.Popen(["python", script])
        processes.append(process)
        time.sleep(1)   
        
def stop_subscribers(signum=None, frame=None):
    print("\n Stopping all subscribers...")
    for process in processes:
        process.terminate()   
    print(" All subscribers stopped.")
    sys.exit(0)

if __name__ == "__main__":
    # Handle Ctrl+C (KeyboardInterrupt)
    signal.signal(signal.SIGINT, stop_subscribers)

    start_subscribers()

    print("Subscribers are running... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)