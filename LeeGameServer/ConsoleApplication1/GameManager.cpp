#include "stdafx.h"
#include "GameManager.h"

#include "NetworkManager.h"

void GameManager::Init() {
	Timer::Create(1, true);
	building.Init();

	self = this;
}

void GameManager::Update(float dt) {
	IsEveryPlayerDisconnected();
	Timer::Tick(dt);

	if (getPlayerCnt() > Player::GetTotalPlayerCnt()) {
		building.SendFurnitureData();
		players.push_back(new Player());
		for (int i = 0; i < players.size(); i++)
		{
			if (!players[i] || players[i]->IsDead()) 
				continue;
			players[i]->SendPlayerPos();
		}
		SendFurnitureState();
	}


	for (auto player : players) {
		if (!player) continue;
		player->Update(dt);
	}

	if (Timer::IsEnd(0)) {
		// 1�ʰ� ��������

		// ����ִ� ������ �ϳ����� �˻�


		// ���� ���� ����
		ScorePacket p;
		p.scores.resize(Player::GetTotalPlayerCnt());
		for (auto player : players) {
			if (!player) continue;
			if (player->score.Update()) {
				// ������ �̰�ٸ� ��������
				WinPlayerIdPacket winPlayerIdPacket;
				winPlayerIdPacket.winPlayerId = player->id;
				SendWinPlayerIdPacketToClients(winPlayerIdPacket);
				//players.resize(0);
				Reset();
			}
			if(player->id < p.scores.size())
				p.scores[player->id] = player->score.score;
		}
		SendPlayersScoreToClients(p);
	}
}

void GameManager::UpdatePlayerInput(ClientKeyInputPacket packet) {
	for (auto player : players) {
		if(player)
		if (player->SetInput(packet))
			break;
	}
}

void GameManager::SendFurnitureState() {
	for (size_t i = 0; i < building.furnitures.size(); i++)
	{
		if (!building.furnitures[i]->interactPlayer)
			continue;
		InteractPacket p;
		p.interactPlayerId = building.furnitures[i]->interactPlayer->id;
		p.interactedObjId = building.furnitures[i]->id;
		SendInteractPacketToClients(p);
	}
	cout << "���� ���� ����" << endl;
}

void GameManager::KillPlayer(int idx) {
	players[idx]->Suicide();
}

GameManager* GameManager::Self() {
	return self;
}

bool GameManager::IsEveryPlayerDisconnected() {
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
		return true;
	}
	return false;
}

void GameManager::Reset() {
	//for (int i = 0; i < players.size(); i++)
	//{
	//	delete players[i];
	//}
	//players.resize(0);

	setPlayerCnt(0);

	Player::Reset();
	InteractObj::Reset();

	//CloseAllClients();

	cout << "��� Ŭ���̾�Ʈ�� ���� ���µ�" << endl;
}

GameManager* GameManager::self = nullptr;
