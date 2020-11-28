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
		for (int i = 0; i < players.size(); i++)
		{
			if (!players[i] || players[i]->IsDead()) 
				continue;
			players[i]->SendPlayerPos();
		}
		players.push_back(new Player());
		SendFurnitureState();
	}


	for (auto player : players) {
		if (!player) continue;
		player->Update(dt);
	}

	if (Timer::IsEnd(0)) {
		// 1�ʰ� ��������

		// ����ִ� ������ �ϳ����� �˻�
		for (int i = 0; i < players.size(); i++)
		{
			if (!players[i] || players[i]->IsDead())
				continue;
			players[i]->SendPlayerPos();
		}
		//SendFurnitureState();

		// ���� ���� ����
		if(!players.empty())
			scorePacket.scores.resize(Player::GetTotalPlayerCnt());
		for (auto player : players) {
			if (!player) continue;
			if (player->UpdateScore()) {
				// ������ �̰�ٸ� ��������
				WinPlayerIdPacket winPlayerIdPacket;
				winPlayerIdPacket.winPlayerId = player->id;
				SendWinPlayerIdPacketToClients(winPlayerIdPacket);
				//players.resize(0);
				cout << "�¸��� �÷��̾�� " << player->id << endl;
				Reset();
				break;
			}
			if(player->id < scorePacket.scores.size())
				scorePacket.scores[player->id] = player->score.score;
		}
		SendPlayersScoreToClients(scorePacket);
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
	for (int i = 0; i < InteractObjManager::interactObjs.size(); i++)
	{
		if (InteractObjManager::interactObjs[i]->interactPlayer == players[idx]) {
			InteractObjManager::interactObjs[i]->interactPlayer = nullptr;
			break;
		}
	}
	delete players[idx];
	players.erase(players.begin() + idx);
	
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
	for (int i = 0; i < players.size(); i++)
	{
		delete players[i];
	}
	players.resize(0);

	setPlayerCnt(0);

	Player::Reset();
	InteractObj::Reset();

	//CloseAllClients();

	cout << "���� ���� ���� ����" << endl;
}

GameManager* GameManager::self = nullptr;
