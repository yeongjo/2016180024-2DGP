#include "stdafx.h"
#include "GameManager.h"

#include "NetworkManager.h"

void GameManager::Init(int playerCnt) {
	Timer::Create(1, true);
	building.Init();
	players.resize(playerCnt);
	self = this;
}

void GameManager::Update(float dt) {
	Timer::Tick(dt);

	for (auto& player : players) {
		player.Update(dt);
	}

	if (Timer::IsEnd(0)) {
		// 1초가 지났으면
		// 유저 점수 증가
		ScorePacket p;
		for (auto& player : players) {
			if (player.score.Update()) {
				// 누군가 이겼다면 게임종료
				WinPlayerIdPacket winPlayerIdPacket;
				winPlayerIdPacket.winPlayerId = player.id;
				SendWinPlayerIdPacketToClients(winPlayerIdPacket);
				return;
			}
			p.scores.push_back(player.score.score);
		}
		SendPlayersScoreToClients(p);
	}
}

void GameManager::UpdatePlayerInput(ClientKeyInputPacket packet) {
	for (auto& player : players) {
		if (player.SetInput(packet))
			break;
	}
}

GameManager* GameManager::Self() {
	return self;
}

GameManager* GameManager::self = nullptr;
