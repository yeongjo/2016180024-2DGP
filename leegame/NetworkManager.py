import socket
import sys
import json
from numpy import unicode
import GameManager
import time
import easygui  # ip입력 받는 입력상자

is_connected = False

# 패킷 타입들
PACKETTYPE_PLAYER = 0
PACKETTYPE_INTERACT = 1
PACKETTYPE_CLINETKEYINPUT = 2
PACKETTYPE_SCORE = 3
PACKETTYPE_WINPLAYERID = 4
PACKETTYPE_MAPDATA = 5
PACKETTYPE_PLAYERID = 6

# 패킷 크기
MAX_PACKET_SIZE = 1000

# 패킷 주고받을거
RecvPacket = 0
# SendPacket = 0

# 패킷내용들
player_id, pos = -1, -1
interactPlayerId, interactedObjId = -1, -1
CKI_key, CKI_id, CKI_isDown = -1, -1, -1
scores = -1
winPlayerId = -1
furniturePos = -1
my_id = -1


# 클라이언트가 누른키 JSON으로 변환하고 패킷으로만듬
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


# 서버로 부터 패킷 받아오고 패킷 타입에 따라 분류함
def RecvClientPacketFromServerAndClassifyByType():
    global RecvPacket
    rev = client_socket.recv(MAX_PACKET_SIZE)
    RecvPacket = unicode(rev, errors='ignore')
    terminator = RecvPacket.index('\x00')
    RecvPacket = RecvPacket[:terminator]
    RecvPacket = json.loads(RecvPacket)

    global player_id, pos, interactPlayerId, interactedObjId, CKI_key, CKI_id, \
        CKI_isDown, scores, winPlayerId, furniturePos, my_id
    if RecvPacket["type"] == PACKETTYPE_PLAYER:
        player_id = RecvPacket["id"]
        pos = [RecvPacket["posx"], RecvPacket["posy"]]
    elif RecvPacket["type"] == PACKETTYPE_INTERACT:
        interactPlayerId = RecvPacket["interactPlayerId"]
        interactedObjId = RecvPacket["interactedObjId"]
    elif RecvPacket["type"] == PACKETTYPE_CLINETKEYINPUT:
        CKI_key = RecvPacket["key"]
        CKI_id = RecvPacket["id"]
        CKI_isDown = RecvPacket["isDown"]
    elif RecvPacket["type"] == PACKETTYPE_SCORE:
        scores = RecvPacket["scores"]
    elif RecvPacket["type"] == PACKETTYPE_WINPLAYERID:
        winPlayerId = RecvPacket["winPlayerId"]
    elif RecvPacket["type"] == PACKETTYPE_MAPDATA:
        furniturePos = [RecvPacket["furniturePosX"], RecvPacket["furniturePosY"]]
    elif RecvPacket["type"] == PACKETTYPE_PLAYERID and my_id == -1:
        my_id = RecvPacket["PlayerId"]
        print("나의 ID는 ", my_id, "이다.")


def PrintPacketInfo():
    print("---------PACKET PREVIEW---------")
    print("나는", my_id, "번째 플레이어")
    print("PLAYER \t\t\t:", player_id, pos)
    print("INTERACT \t\t:", interactPlayerId, interactedObjId)
    print("CLINETKEYINPUT \t:", CKI_key, CKI_id, CKI_isDown)
    print("SCORE \t\t\t:", scores)
    print("WINPLAYERID \t:", winPlayerId)
    print("MAPDATA \t\t:", furniturePos)


# ipAddress = easygui.enterbox("IP 주소 입력해주세요")
# portNum = easygui.enterbox("포트번호 입력 해주세요")
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
    RecvClientPacketFromServerAndClassifyByType()
    SendClientKeyInputPacketToServer(SendPacket)
    PrintPacketInfo()
    SendPacket.key += 1
    time.sleep(.1)

# client_socket.close()

quit()

# 너가 넣어저야할거
GameManager.update_ui((12, 43, 552))
GameManager.update_player_pos(player_id, pos)
GameManager.update_interact_state(interactPlayerId, interactedObjId)
GameManager.set_my_player_id(player_id)
GameManager.boardcast_win_player(winPlayerId)
