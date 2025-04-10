import time
import random
import threading
import paho.mqtt.client as mqtt_client
import lib
import logger

class MqttClient:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            lib.log("MqttClient __new__ is called")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        lib.log("MqttClient __init__ is called")
        
        self.host = kwargs.get('host')
        if not self.host:
            raise Exception("Not found mqtt server's host")
        
        self.port = kwargs.get('port')
        if not self.port:
            raise Exception("Not found mqtt server's port")
        
        self.username = kwargs.get('username', '')
        self.passwd = kwargs.get('passwd', '')
        self.topic = kwargs.get('topic')
        self.onmessage = kwargs.get('onmessage')
        self.client = None
        self.reconnect_delay = 1
        self.max_reconnect_delay = 120
        self.create_client()


    def create_client(self):
        client_id = f"mqtt_client_{random.randint(0, 1000)}"
        try:
            self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id=client_id, clean_session=False)
        except:
            self.client = mqtt_client.Client(client_id=client_id, clean_session=False)
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)

    def connect(self):
        if self.username and self.passwd:
            self.client.username_pw_set(self.username, self.passwd)
        try:
            self.client.connect(host=self.host, port=self.port, keepalive=60)
        except Exception as e:
            lib.log(f"MQTT - Connection failed: {e}")
            self.schedule_reconnect()

    def schedule_reconnect(self):
        lib.log(f"MQTT - Scheduling reconnect in {self.reconnect_delay} seconds")
        threading.Timer(self.reconnect_delay, self.connect).start()
        self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            lib.log(f"MQTT - Connected to MQTT Broker")
            self.reconnect_delay = 1  # Reset reconnect delay on successful connection
            if self.topic:
                self.subscribe(self.topic)
        else:
            lib.log(f"MQTT - Failed to connect, Returned code: {rc}")
            self.schedule_reconnect()

    def on_disconnect(self, client, userdata, rc):
        lib.log(f"MQTT - Disconnected with result code {rc}")
        self.schedule_reconnect()

    def on_log(self, client, userdata, level, buf):
        lib.log(f"MQTT - log: {buf}")

    def on_message(self, client, userdata, msg):
        logger.Logger._LOGGER.info(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        if callable(self.onmessage):
            lib.log("Forwarding message to external handler")
            self.onmessage(client, userdata, msg)
        else:
            lib.log("No external message handler defined")

    def subscribe(self, topic):
        try:
            self.client.subscribe(topic)
            logger.Logger._LOGGER.info(f"MQTT - Subscribed to: {topic}")
        except Exception as e:
            lib.log(f"MQTT - Subscription failed: {e}")

    def publish(self, topic, msg):
        try:
            if isinstance(msg, dict):
                msg = lib.jsonencode(msg)
            logger.Logger._LOGGER.info(f"MQTT - Publishing to {topic}: {msg}")
            self.client.publish(topic, msg)
        except Exception as e:
            lib.log(f"MQTT - Publish failed: {e}")

    def check_connection(self):
        if not self.client.is_connected():
            lib.log("MQTT - Client is not connected. Attempting to reconnect...")
            self.connect()
        else:
            lib.log("MQTT - Client is connected")

    def start_connection_check(self, interval=60):
        def check_periodically():
            while True:
                self.check_connection()
                time.sleep(interval)
        
        check_thread = threading.Thread(target=check_periodically)
        check_thread.daemon = True
        check_thread.start()

    def run(self):
        self.connect()
        self.client.loop_forever()  # Changed from loop_start() to loop_forever()

    def input_and_publish(self):
        while True:
            try:
                input("Press Enter to input a message...")
                msg = input("Enter message to publish: ")
                self.publish(self.topic, msg)
            except Exception as e:
                lib.log(f"Error in input_and_publish: {e}")
