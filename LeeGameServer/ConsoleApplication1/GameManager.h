#pragma once
#include "Player.h"
#include "Timer.h"

class GameManager {
public:
	void Init(int playerCnt);

	void Update(float dt);
private:
	vector<Player> players;
	Building building;
};

