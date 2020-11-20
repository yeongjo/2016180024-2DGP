import socket
import sys
import json
import GameManager

is_connected = False

HOST = '127.0.0.1'
PORT = 9000
MAX_SIZE = 200

m = '{ "furniturePosX" : [1.0,12.0], "furniturePosY" : [0.0,3.0], "type" : 5 }'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))
client_socket.sendall(bytes(m, encoding="utf-8"))

client_socket.close()
# received = client_socket.recv(MAX_SIZE)

quit()

# 너가 넣어저야할거
# GameManager.update_ui((12, 43, 552))
# GameManager.update_player_pos(id, pos)
# GameManager.update_interact_state(interactor_id, target_id):
# GameManager.set_my_player_id(id)
# GameManager.boardcast_win_player(win_player_idx):

PACKETTYPE_PLAYER = 1
PACKETTYPE_INTERACT = 2
PACKETTYPE_CLINETKEYINPUT = 3
PACKETTYPE_SCORE = 4
PACKETTYPE_WINPLAYERID = 5


class ClientKeyInputPacket:
    def __init__(self):
        self.type = PACKETTYPE_CLINETKEYINPUT
        self.id = GameManager.my_player_id  # 플레이어마다 다른 고유한 번호
        self.key = 0
        self.isDown = False


def TcpSendClientKeyInputPacketToServer(packet):
    pass
