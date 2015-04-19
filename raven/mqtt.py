import paho.mqtt.client as mqtt
import json
import logging
from ConfigParser import RawConfigParser

kLog = logging.getLogger(__name__)

class MosquittoClient(object):
	def __init__(self, config_path):
		config = RawConfigParser()
		config.read(config_path)
		client = mqtt.Client(config.get('mqtt', 'client_name'), True)
		client.username_pw_set(config.get('mqtt', 'username'), config.get('mqtt', 'password'))
		client.tls_set(config.get('mqtt', 'ca_cert'))
		if config.get('mqtt','hostname') in ('localhost', '127.0.0.1', '::1'):
			client.tls_insecure_set(True)
		self.config = config
		self.client = client

	def start(self):
		hostname = self.config.get('mqtt', 'hostname')
		port = self.config.get('mqtt', 'port')
		kLog.debug("Connecting to MQTT server at {}:{}".format(hostname, port))
		self.client.connect(hostname, port)
		self.client.loop_start()
		kLog.info("Connected to MQTT server")

	def stop(self):
		kLog.debug("Disconnecting from MQTT server")
		self.client.disconnect()
		self.client.loop_stop()
		kLog.info("Disconnected from MQTT server")

	def publish(self, topic, timestamp, value):
		payload = json.dumps({'ts': timestamp, 'val': value})
		kLog.debug("Publishing {} to {}".format(payload, topic))
		self.client.publish(topic, payload)