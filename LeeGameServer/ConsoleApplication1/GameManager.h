#pragma once
#include "Player.h"
#include "Timer.h"

class GameManager {
public:
	void Init();

	void Update(float dt);

	void UpdatePlayerInput(ClientKeyInputPacket packet);

	static GameManager* Self();

	vector<Player*> players;
	Building building;
private:
	void Reset();
	
	static GameManager *self;
	float delaySendFurnitureTime = 0;
	float defaultDelaySendFurnitureTime = 1;
};

