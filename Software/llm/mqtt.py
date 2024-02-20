import time
import paho.mqtt.client as mqtt


class MQTT:
    def __init__(self, mqtt_broker="192.168.49.74", mqtt_port=1883):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(mqtt_broker, mqtt_port)
        self.client.loop_start()

    def send_msg(self, topic, message):
        try:
            self.client.publish(topic, message)
        except:
            pass

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    def release(self):
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == '__main__':
    mqtt_client = MQTT(mqtt_broker="192.168.49.74", mqtt_port=1883)
    mqtt_client.send_msg("/seeebot", "service_enabled_nlp=false The models are installed and configured if they are uncommented in")
    time.sleep(1)
    # while True:
    #     mqtt_client.send_msg("/seeebot", "Hello")
    #     time.sleep(2)

