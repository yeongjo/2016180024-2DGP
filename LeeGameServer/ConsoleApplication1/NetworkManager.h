#pragma once
#include "Packets.h"
class MapDataPacket;

int getPlayerCnt();

DWORD WINAPI ProcessClient(LPVOID arg);

//처음 접속한 클라에게 아이디 줌
void SendPlayerIDPacketToClients(int id);
//클라에게 위치 보냄
void SendChangedPlayerPositionToClients(PlayerPacket player);
//클라에게 상호작용한거 보냄
void SendInteractPacketToClients(InteractPacket interact);
//클라에게 승리 진행률 보냄
void SendPlayersScoreToClients(ScorePacket score);
//클라에게 게임승리 조건 달성됬다고 보냄
void SendWinPlayerIdPacketToClients(WinPlayerIdPacket winplayer);
//클라에게 맵데이터 보냄
void SendMapDataPackets(MapDataPacket mapData);


int InitServerSocket();

