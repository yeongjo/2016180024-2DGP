#pragma once
#include "Packets.h"
class MapDataPacket;

DWORD WINAPI ProcessClient(LPVOID arg);


//Ŭ�󿡰� ��ġ ����
void SendChangedPlayerPositionToClients(PlayerPacket player);
//Ŭ�󿡰� ��ȣ�ۿ��Ѱ� ����
void SendInteractPacketToClients(InteractPacket interact);
//Ŭ�󿡰� �¸� ����� ����
void SendPlayersScoreToClients(ScorePacket score);
//Ŭ�󿡰� ���ӽ¸� ���� �޼���ٰ� ����
void SendWinPlayerIdPacketToClients(WinPlayerIdPacket winplayer);
//Ŭ�󿡰� �ʵ����� ����
void SendMapDataPackets(MapDataPacket mapData);


int InitServerSocket();

