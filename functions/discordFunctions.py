import json
import socket
from enum import Enum
import re
import os
import struct
import uuid
import time

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2

# https://discord.com/developers/docs/events/gateway-events#activity-object-activity-types
class Activity(Enum):
    Playing = 0
    Streaming = 1
    Listening = 2
    Watching = 3
    Custom = 4
    Competing = 5

class DiscordRPC():
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.user = {}
        self.connected = False
        
    def setupConnection(self) -> bool:
        self.ipc = UnixPipe(self.app_id)
        if not self.ipc.connected:
            print("Failed to connect to Discord IPC")
            return False
        self.user = self.ipc.handshake()

        if not self.user:
            print("Failed to complete handshake with Discord")
            return False
        self.connected = True
        return True
    
    def disconnect(self):
        if self.connected and self.ipc:
            self.ipc.disconnect()
            self.connected = False

    def setActivity(self, activity: dict):
        if not self.connected or not self.ipc:
            print("Not connected to Discord RPC")
            return False
        
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": os.getpid(),
                "activity": activity
            },
            "nonce": str(uuid.uuid4())
        }

        self.ipc.send(payload)
        self.ipc.recv()
        
    def formatMusicActivity(self, plex_data: dict) -> dict:
        if not plex_data:
            return {}
        
        # print(plex_data)
        
        activity = {
            "state": f"{plex_data.get('artist')}",
            "details": f"{plex_data.get('title')}",
            "type": 2,
            "timestamps": {
                "start": int(time.time() * 1000) - plex_data.get('duration_offset', 0),
                "end": int(time.time() * 1000) + (plex_data.get('duration', 0) - plex_data.get('duration_offset', 0)) if plex_data.get('duration') else None
            },
            "assets": {
                # "large_image": "plexamp",
                # "large_text": f"{plex_data.get('title')}",
                # "small_image": "plexamp",
                # "small_text": "Plexamp",
                # "small_url": "https://plexamp.com",
            }
        }
        return activity

class UnixPipe:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.connected = False

        self.socket = socket.socket(socket.AF_UNIX)

        base_path = path = os.environ.get('XDG_RUNTIME_DIR') or os.environ.get('TMPDIR') or os.environ.get('TMP') or os.environ.get('TEMP') or '/tmp'
        base_path = re.sub(r'\/$', '', path) + '/discord-ipc-{0}'

        for i in range(10):
            path = base_path.format(i)

            try:
                self.socket.connect(path)
                break
            except FileNotFoundError:
                continue

        else:
            self.connected = False
            return
        
        self.connected = True
        print(f"Connected to {path}")


    def recv(self):
        recv_data = self.socket.recv(1024)
        # enc_header = recv_data[:8]
        # dec_header = struct.unpack('<ii', enc_header)
        enc_data = recv_data[8:]
        
        output = json.loads(enc_data.decode('utf-8'))
        return output
    
    def send(self, payload, op=OP_FRAME):
        payload = json.dumps(payload).encode('utf-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.send(payload)

    def handshake(self):
        self.send({'v': 1, 'client_id': self.app_id}, op=OP_HANDSHAKE)
        data = self.recv()

        try:
            if data["cmd"] == "DISPATCH" and data["evt"] == "READY":
                self.user = data["data"]["user"]
                print(f"Connected to Discord as {self.user['username']}#{self.user['discriminator']}")
                return True
        except KeyError:
            pass

    def disconnect(self):
        try:
            self.send({}, OP_CLOSE)
            self.socket.close()
        except Exception as e:
            print(f"Error disconnecting: {e}")

        self.socket = None
        self.connected = False


    






