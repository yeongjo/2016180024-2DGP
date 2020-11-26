#pragma once
#include "Player.h"
#include "Timer.h"

class GameManager {
public:
	void Init(int playerCnt);

	void Update(float dt);

	void UpdatePlayerInput(ClientKeyInputPacket packet);

	static GameManager* Self();

	vector<Player> players;
	Building building;
private:
	static GameManager *self;
};

