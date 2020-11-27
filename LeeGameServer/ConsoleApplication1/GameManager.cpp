#include "stdafx.h"
#include "GameManager.h"

#include "NetworkManager.h"

void GameManager::Init() {
	Timer::Create(1, true);
	building.Init();

	self = this;
}

void GameManager::Update(float dt) {
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

	for (auto& player : players) {
		player->Update(dt);
	}

	if (Timer::IsEnd(0)) {
		// 1�ʰ� ��������

		// ����ִ� ������ �ϳ����� �˻�


		// ���� ���� ����
		ScorePacket p;
		for (auto& player : players) {
			if (player->score.Update()) {
				// ������ �̰�ٸ� ��������
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

	CloseAllClients();
}

GameManager* GameManager::self = nullptr;
