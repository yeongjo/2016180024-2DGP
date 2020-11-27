#pragma once
#include "Player.h"
#include "Timer.h"

class GameManager {
public:
	void Init();

	void Update(float dt);

	void UpdatePlayerInput(ClientKeyInputPacket packet);

	void SendFurnitureState();

	void KillPlayer(int idx);

	void Reset();

	static GameManager* Self();

	vector<Player*> players;
	Building building;
	bool isEnd = false;
private:
	bool IsEveryPlayerDisconnected();
	
	static GameManager *self;
	float delaySendFurnitureTime = 0;
	float defaultDelaySendFurnitureTime = 1;
};

