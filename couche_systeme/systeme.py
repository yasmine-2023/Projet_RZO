
import errno
import os
import socket
import struct
import subprocess
from typing import TypedDict, Optional

# from class_types.buildind_types import BuildingTypes
# from class_types.network_commands_types import NetworkCommandsTypes
# from class_types.road_types import RoadTypes



# from class_types.buildind_types import BuildingTypes

class Header(TypedDict):
    player_id: int
    command: int
    object_size: int
    id_object: int

class Message(TypedDict):
    header: Header
    data: any


class RiskMsg(TypedDict):
    fire_level: int
    damage_level: int
    building_position: list[int, int]

class SystemInterface:
    instance = None

    def __init__(self):
        self.message_read = None
        self.message_write = None
        self.connection = None
        self.sock = None
        self.player_id = 0
        self.ip = None

        self.is_online = False

    def init_listen(self):
        from mon_code.game.jeu import jeu
        client_path = "./client_c" #a changer
        if not os.path.exists(client_path):
            print("Error C client not found, please run `make` before play online")
            return

        socket_address = "/tmp/socket"
        if os.path.exists(socket_address):
            os.remove(socket_address)

        # Create a Unix domain socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket
        self.sock.bind(socket_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # Wait for a connection
        print(f"Waiting for a connection on {socket_address}")

        # Run subprocess here to wait connection before lauch it

        if self.ip:
            c_file = [client_path,self.ip]
        else:
            c_file = [client_path]

        self.pid = subprocess.Popen(c_file)

        connection, client_address = self.sock.accept()
        self.connection = connection

        message = self.read_message(block=True)
        if not message:
            print("error receive C connection")
            return

        if message["header"]["command"] != 400:
            print("bad receive packet")
            return

        self.player_id = message["header"]["player_id"]

        print(f"Found C connection, player id : {self.player_id}")
        j = jeu.get_instance()
        j.set_all_player_id(self.player_id)
        self.set_is_online(True)

    def send_message(self, command, id_object, data, encode=True):
        if not self.connection:
            return

        if encode:
            data = data.encode()

        if data:
            object_size = len(data)

            format_send_types = f"=H H L L {object_size}s"
            sending_message = struct.pack(format_send_types,
                                          self.player_id, command,
                                          object_size,
                                          id_object,
                                          data)

        else:
            format_send_types = f"=H H L L"
            sending_message = struct.pack(format_send_types,
                                          self.player_id, command,
                                          0,
                                          id_object)

        return self.connection.sendall(sending_message)

    def read_message(self,block: bool = False) -> Optional[Message]:
        if self.connection is None:
            return None

        header_size = 12
        if not block:
            self.connection.setblocking(0)

        try:
            binary_received_header = self.connection.recv(header_size)
            if binary_received_header == b'':
                return None
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            self.connection.setblocking(1)
            return None

        self.connection.setblocking(1)


        header = self.unpack_header(binary_received_header)

        if header["object_size"]:
            binary_received_data = self.connection.recv(header["object_size"], socket.MSG_WAITALL)
            data = self.unpack_data(binary_received_data, header["object_size"])
        else:
            data = None


        self.message_read: Message = {
            "header": header,
            "data": data
        }

        print(self.message_read)
        return self.message_read


    def unpack_data(self, binary_received_data, data_len):
        format = f"={data_len}s"
        #print(format, binary_received_data)
        data = struct.unpack(format, binary_received_data)
        return data
    def unpack_header(self, binary_received_header) -> Header:
        header = struct.unpack("=H H L L", binary_received_header)
        temp_dict = {
            "player_id": header[0],
            "command": header[1],
            "object_size": header[2],
            "id_object": header[3]
        }

        return temp_dict

    def close_socket(self):
        self.connection.close()
        self.sock.close()

  