#pragma once
#include "Packets.h"
class MapDataPacket;

int getPlayerCnt();

void setPlayerCnt(int cnt);

DWORD WINAPI ProcessClient(LPVOID arg);

//ó�� ������ Ŭ�󿡰� ���̵� ��
void SendPlayerIDPacketToClients(int id);
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
//��� Ŭ�� ���� ����
void CloseAllClients();

int InitServerSocket();

