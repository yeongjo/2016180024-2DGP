#pragma once
class MapDataPacket;

class NetworkManager {
public:
	static void TcpSendMapDataPacket(MapDataPacket mapData);
};

