import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # type: ignore

# from paho.mqtt.enums import CallbackAPIVersion

client = mqtt.Client()  # Removed CallbackAPIVersion.VERSION1


parent_topic = "shellies/shellydimmer2-EC64C9C2EFE2"

topics = [
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/status',
    'shellies/shellydimmer2-EC64C9C2EFE2/temperature',
    'shellies/shellydimmer2-EC64C9C2EFE2/temperature_f',
    'shellies/shellydimmer2-EC64C9C2EFE2/overtemperature',
    'shellies/shellydimmer2-EC64C9C2EFE2/overpower',
    'shellies/shellydimmer2-EC64C9C2EFE2/loaderror',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/power',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/energy',
    'shellies/shellydimmer2-EC64C9C2EFE2/input/0',
    'shellies/shellydimmer2-EC64C9C2EFE2/input/1',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/set',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/status',
    'shellies/shellydimmer2-EC64C9C2EFE2/temperature',
    'shellies/shellydimmer2-EC64C9C2EFE2/temperature_f',
    'shellies/shellydimmer2-EC64C9C2EFE2/overtemperature',
    'shellies/shellydimmer2-EC64C9C2EFE2/overpower',
    'shellies/shellydimmer2-EC64C9C2EFE2/loaderror',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/power',
    'shellies/shellydimmer2-EC64C9C2EFE2/light/0/energy',
    'shellies/shellydimmer2-EC64C9C2EFE2/input/0',
    'shellies/shellydimmer2-EC64C9C2EFE2/input/1',
]

topics = [f'{parent_topic}/{sub_topic}' for sub_topic in sub_topics]

def print_user_data(client, userdata):
    print(f'Userdata: {userdata}')
    print(f'Client: {client}')

def on_subscribe(client, userdata, mid, granted_qos):
    # print_user_data(client, userdata)
    print(f'Subscribed: {mid} {granted_qos}')

def on_connect(client, userdata, flags, reason_code, properties=None):
    # print_user_data(client, userdata)
    # print(f'Flags: {flags}')
    # print(f'Connected: {reason_code} {properties}')
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, message):
    # print_user_data(client, userdata)
    print(f'{message.topic}: {message.payload.decode()}')

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect("192.168.1.8", 1883)

# Start the loop to process network traffic
client.loop_forever()

