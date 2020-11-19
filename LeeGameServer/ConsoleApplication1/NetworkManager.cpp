#include "stdafx.h"
#include "NetworkManager.h"

#include "Packets.h"

void NetworkManager::TcpSendMapDataPacket(MapDataPacket mapData) {
	mapData.type = EPacketType::MapData;
	
}
