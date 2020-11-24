import socket
import sys
import json
from numpy import unicode

import GameManager

import time
import easygui      # ip입력 받는 입력상자

is_connected = False

# 패킷 타입들
PACKETTYPE_PLAYER = 0
PACKETTYPE_INTERACT = 1
PACKETTYPE_CLINETKEYINPUT = 2
PACKETTYPE_SCORE = 3
PACKETTYPE_WINPLAYERID = 4
PACKETTYPE_MAPDATA = 5

# 패킷 크기
MAX_PACKET_SIZE = 1000

# 패킷 주고받을거
RecvPacket = 0
# SendPacket = 0

# 패킷내용들
player_id, pos = 0, 0
interactPlayerId, interactedObjId = 0, 0
CKI_key, CKI_id, CKI_isDown = 0, 0, 0
scores = 0
winPlayerId = 0
furniturePos = 0


class ClientKeyInputPacket:
    def __init__(self):
        self.type = PACKETTYPE_CLINETKEYINPUT
        # self.id = GameManager.my_player_id  # 플레이어마다 다른 고유한 번호
        self.id = 1
        self.key = 0
        self.isDown = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


# 입력키 패킷으로 만들어서 서버한테 전송
def SendClientKeyInputPacketToServer(packet):
    client_socket.sendall(bytes(packet.toJSON(), encoding="utf-8"))


# 서버로 부터 패킷 받아옴
def RecvClientPacketFromServer():
    global RecvPacket
    rev = client_socket.recv(MAX_PACKET_SIZE)
    RecvPacket = unicode(rev, errors='ignore')
    terminator = RecvPacket.index('\x00')
    RecvPacket = RecvPacket[:terminator]
    RecvPacket = json.loads(RecvPacket)


def PacketParsing(packet):
    global player_id, pos, interactPlayerId, interactedObjId, \
        CKI_key, CKI_id, CKI_isDown, scores, winPlayerId, furniturePos
    if packet["type"] == PACKETTYPE_PLAYER:
        player_id = packet["id"]
        pos = [packet["posx"], packet["posy"]]
    elif packet["type"] == PACKETTYPE_INTERACT:
        interactPlayerId = packet["interactPlayerId"]
        interactedObjId = packet["interactedObjId"]
    elif packet["type"] == PACKETTYPE_CLINETKEYINPUT:
        CKI_key = packet["key"]
        CKI_id = packet["id"]
        CKI_isDown = packet["isDown"]
    elif packet["type"] == PACKETTYPE_SCORE:
        scores = packet["scores"]
    elif packet["type"] == PACKETTYPE_WINPLAYERID:
        winPlayerId = packet["winPlayerId"]
    elif packet["type"] == PACKETTYPE_MAPDATA:
        furniturePos = [packet["furniturePosX"], packet["furniturePosY"]]


def PrintPacketInfo():
    print("---------PACKET PREVIEW---------")
    print("PLAYER \t\t\t:", player_id, pos)
    print("INTERACT \t\t:", interactPlayerId, interactedObjId)
    print("CLINETKEYINPUT \t:", CKI_key, CKI_id, CKI_isDown)
    print("SCORE \t\t\t:", scores)
    print("WINPLAYERID \t:", winPlayerId)
    print("MAPDATA \t\t:", furniturePos)


#ipAddress = easygui.enterbox("IP 주소 입력해주세요")
#portNum = easygui.enterbox("포트번호 입력 해주세요")
ipAddress = '192.168.1.176'
portNum = 9000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddress, int(portNum)))


# 테스트 패킷
SendPacket = ClientKeyInputPacket()
SendPacket.key = 2
SendPacket.id = 1.0
SendPacket.isDown = False


while True:
    RecvClientPacketFromServer()
    PacketParsing(RecvPacket)
    SendClientKeyInputPacketToServer(SendPacket)
    PrintPacketInfo()
    SendPacket.key += 1
    time.sleep(.5)


# client_socket.close()

quit()

# 너가 넣어저야할거
GameManager.update_ui((12, 43, 552))
GameManager.update_player_pos(player_id, pos)
GameManager.update_interact_state(interactPlayerId, interactedObjId)
GameManager.set_my_player_id(player_id)
GameManager.boardcast_win_player(winPlayerId)
