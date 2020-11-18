#include "stdafx.h"
#include "GameManager.h"

void GameManager::Init(int playerCnt) {
	Timer::Create(1, true);
	building.Init();
	players.resize(playerCnt);
}

void GameManager::Update(float dt) {
	Timer::Tick(dt);

	for (auto& player : players) {
		player.Update(dt);
	}

	if (Timer::IsEnd(0)) {
		// 1�ʰ� ��������
		// ���� ���� ����
		for (auto& player : players) {
			if (player.score.Update()) {
				// ������ �̰�ٸ� ��������

				return;
			}
		}
	}
}
