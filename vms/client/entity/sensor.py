import os
import time
import random
import json
import paho.mqtt.client as mqtt
from datetime import datetime

class Sensor:
    def __init__(self, name, interval):
        self.name = name
        self.interval = interval

    def generate(self):
        return round(random.uniform(10.0, 30.0), 2)

    def read(self):
        return {
            "name": self.name,
            "value": self.generate(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

class TemperatureSensor(Sensor):
    def generate(self):
        return round(random.uniform(20.0, 40.0), 2)

class PressureSensor(Sensor):
    def generate(self):
        return round(1000 + random.random() * 50, 2)

class CurrentSensor(Sensor):
    def generate(self):
        return round(random.uniform(0.1, 10.0), 2)

class HumiditySensor(Sensor):
    def generate(self):
        return round(random.uniform(30.0, 90.0), 2)

SENSOR_TYPES = {
    "temperature": TemperatureSensor,
    "pressure": PressureSensor,
    "current": CurrentSensor,
    "humidity": HumiditySensor,
}

# Параметры из переменных окружения
sensor_type = os.getenv("SENSOR_TYPE", "temperature")
sensor_name = os.getenv("SENSOR_NAME", "sensor1")
interval = int(os.getenv("INTERVAL", 5))
broker_host = os.getenv("BROKER_HOST", "192.168.0.150")
broker_port = int(os.getenv("BROKER_PORT", 1883))

SensorClass = SENSOR_TYPES.get(sensor_type, Sensor)
sensor = SensorClass(sensor_name, interval)

client = mqtt.Client()
client.connect(broker_host, broker_port, 60)

topic = f"/sensor/{sensor_type}"

while True:
    payload = json.dumps(sensor.read())
    client.publish(topic, payload)
    print(json.dumps(sensor.read(), indent=2))
    print(f"[{sensor_name}] -> {topic}: {payload}")
    time.sleep(interval)
