"""Pull meshtastic info over wifi into homeasssistant webhook
"""

from time import sleep
import json
import os

import meshtastic
import meshtastic.tcp_interface

import requests

from pubsub import pub

from google.protobuf.json_format import MessageToDict

MESHTASTIC_HOST = "192.168.86.65"
HOME_ASSISTANT_HOST = "192.168.86.52"
TIMEOUT = 20  # seconds to wait for info response
WEBHOOK_URL = f"http://{HOME_ASSISTANT_HOST}:8123/api/webhook/{os.environ['WEBHOOK_ID']}"

def on_connection(interface, topic=pub.AUTO_TOPIC):
    info = get_info_as_dict(interface)
    print(json.dumps(info, indent=2))
    push_info_to_ha(info)
    interface.close()

def get_info_as_dict(interface):
    info = {
            "long_name": interface.getLongName(),
            "short_name": interface.getShortName(),
            "my_info": MessageToDict(interface.myInfo),
            "metadata": MessageToDict(interface.metadata),
            "nodes": {}
            # missing: channel info, preferences, module preferences
    }
    for node in interface.nodes.values():
        info["nodes"][node["user"]["id"]] = node
    return info

def push_info_to_ha(info):
    try:
        response = requests.post(WEBHOOK_URL,
            headers={'Content-Type': "application/json"},
            json=info)
        response.raise_for_status()
        print("Response: ", response.status_code, response.text)
    except Exception as ex:
        print("Error POSTing", ex)

pub.subscribe(on_connection, "meshtastic.connection.established")

try:
    iface = meshtastic.tcp_interface.TCPInterface(MESHTASTIC_HOST)
    sleep(TIMEOUT)
except Exception as ex:
    print(f"Error: Could not connect to {MESHTASTIC_HOST}: {ex}")


