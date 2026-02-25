"""Pull meshtastic info over wifi into homeasssistant webhook
"""

from time import sleep
import json

import meshtastic
import meshtastic.tcp_interface

from pubsub import pub

from google.protobuf.json_format import MessageToDict

MESHTASTIC_HOST="192.168.86.65"
HOME_ASSISTANT_HOST="FIXME"
TIMEOUT=20  # seconds to wait for info response

def on_connection(interface, topic=pub.AUTO_TOPIC):
    info = get_info_as_dict(interface)
    print(json.dumps(info, indent=2))
    interface.close()

def get_info_as_dict(interface):
    info = {
            "long_name": interface.getLongName(),
            "short_name": interface.getShortName(),
            "my_info": MessageToDict(interface.myInfo),
            "metadata": MessageToDict(interface.metadata),
            "nodes": {}
    }
    for node in interface.nodes.values():
        info["nodes"][node["user"]["id"]] = node
    return info

pub.subscribe(on_connection, "meshtastic.connection.established")

try:
    iface = meshtastic.tcp_interface.TCPInterface(MESHTASTIC_HOST)
    sleep(TIMEOUT)
except Exception as ex:
    print(f"Error: Could not connect to {MESHTASTIC_HOST}: {ex}")


