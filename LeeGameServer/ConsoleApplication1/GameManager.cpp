#include "stdafx.h"
#include "GameManager.h"

#include "NetworkManager.h"

void GameManager::Init() {
	Timer::Create(1, true);
	building.Init();

	self = this;
}

void GameManager::Update(float dt) {
	bool isNotNull = false;
	for (int i = 0; i < players.size(); i++)
	{
		if (players[i] != nullptr) {
			isNotNull = true;
			break;
		}
	}
	if (players.size() > 0 && !isNotNull) {
		Reset();
		return;
	}
	Timer::Tick(dt);

	if (getPlayerCnt() > players.size()) {
		//delaySendFurnitureTime += dt;
		//if (delaySendFurnitureTime > defaultDelaySendFurnitureTime) {
		//	delaySendFurnitureTime = 0;
		building.SendFurnitureData();
		players.push_back(new Player());
		for (int i = 0; i < players.size(); i++)
		{
			players[i]->SendPlayerPos();
		}

		//}
		//break;
	}

	if (players.size() == 0) return;


	for (auto player : players) {
		if (!player) continue;
		player->Update(dt);
	}

	if (Timer::IsEnd(0)) {
		// 1초가 지났으면

		// 살아있는 유저가 하나인지 검사


		// 유저 점수 증가
		ScorePacket p;
		for (auto player : players) {
			if (!player) continue;
			if (player->score.Update()) {
				// 누군가 이겼다면 게임종료
				WinPlayerIdPacket winPlayerIdPacket;
				winPlayerIdPacket.winPlayerId = player->id;
				SendWinPlayerIdPacketToClients(winPlayerIdPacket);
				//players.resize(0);
				Reset();
				return;
			}
			p.scores.push_back(player->score.score);
		}
		SendPlayersScoreToClients(p);
	}
}

void GameManager::UpdatePlayerInput(ClientKeyInputPacket packet) {
	for (auto& player : players) {
		if (player->SetInput(packet))
			break;
	}
}

GameManager* GameManager::Self() {
	return self;
}

void GameManager::Reset() {
	for (int i = 0; i < players.size(); i++)
	{
		delete players[i];
	}
	players.resize(0);

	setPlayerCnt(0);

	Player::Reset();
	InteractObj::Reset();

	CloseAllClients();
}

GameManager* GameManager::self = nullptr;
