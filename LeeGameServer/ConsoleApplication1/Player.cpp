#include "stdafx.h"
#include "Player.h"


#include "GameManager.h"
#include "NetworkManager.h"

bool Player::PlayerScore::Update() {
	if (score >= 100) { return true; }
	score += increaseScoreAmount;
	return false;
}

Player::Player() : Obj() {
	id = totalPlayerCnt++;
	PlayersManager::players.push_back(this);
	SetRandomPos();
	SendPlayerPos();
}

void Player::Update(float dt) {
	if (IsDead())
		return;

	auto stair = isInStair();
	if (stayStair != stair) {
		stayStair = stair;
		if (stayStair) {
			isRun = false;
			pos = stayStair->pos;
			//moveDirection = 0;
			SendPlayerPos();
			return;
		}
	}
	
	if (IsMoving() && !stayStair) {
		speed = isRun ? runSpeed : walkSpeed;
		pos.x += speed * dt * (float)moveDirection;
		SendPlayerPos();
	}
}

bool Player::SetInput(ClientKeyInputPacket packet) {
	if (!IsControlable() || id != packet.id) return false;
	if (stayStair) {
		if(packet.isDown)
			MoveInStair(packet.key);
		return true;
	}
	auto value = packet.isDown ? 1 : -1;
	moveDirection -= (packet.key == KEY_A) * value;
	moveDirection += (packet.key == KEY_D) * value;
	if (moveDirection < -1)
		moveDirection = -1;
	if (moveDirection > 1)
		moveDirection = 1;
	lookDirec = moveDirection != 0 ? moveDirection : lookDirec;
	if (moveDirection == 0) {
		SendPlayerPos();
	}
	switch (packet.key) {
	case KEY_H:
		Interact();
		break;
	case KEY_J:
		isRun = packet.isDown;
		break;
	case KEY_K:
		Attack();
		break;
	}

	return true;
}

void Player::TakeDamage(int damage) {
	health -= damage;
}

bool Player::IsDead() const {
	return health <= 0;
}

void Player::Attack() {
	auto attackPos = pos;
	attackPos.x += lookDirec * 100;
	//attackPos.y += 50;
	auto player = PlayersManager::FindNearestPlayer(attackPos, 150, this);
	InteractPacket p;
	p.interactPlayerId = id;
	p.interactedObjId = -1;
	if (player != nullptr && !player->IsDead()) {
		player->TakeDamage(1);
		p.interactedObjId = player->id;
	}
	SendInteractPacketToClients(p);
}

void Player::Interact() {
	auto interactedObj = InteractObjManager::Interact(this);
	InteractPacket p;
	p.interactPlayerId = id;
	p.interactedObjId = interactedObj != nullptr ? interactedObj->id : 1000;
	//if(interactedObj) {
	//	interactedObj->interactPlayer = this;
	//}
	SendInteractPacketToClients(p);
}

void Player::SetRandomPos() {
	pos.x = Random(0, 2) * 1920;
	pos.y = Building::CalculateFloorHeight(Random(0, 6));
}

bool Player::IsMoving() {
	return moveDirection != 0;
}

void Player::SendPlayerPos() {
	PlayerPacket p;
	p.pos = pos;
	p.id = id;
	SendChangedPlayerPositionToClients(p);
}

void Player::Suicide() {
	InteractPacket p;
	p.interactPlayerId = id;
	p.interactedObjId = id;
	SendInteractPacketToClients(p);
	SendInteractPacketToClients(p);
}

int Player::GetTotalPlayerCnt() {
	return totalPlayerCnt;
}

void Player::Reset()
{
	totalPlayerCnt = 0;
}

bool Player::IsControlable() {
	return !IsDead();
}

Stair* Player::isInStair() {
	return GameManager::Self()->building.IsInStair(pos);
}

void Player::MoveInStair(int key) {
	switch (key) {
	case KEY_A:
		pos = stayStair->targetPos[Stair::LEFT];
		moveDirection = -1;
		SendPlayerPos();
		break;
	case KEY_D:
		pos = stayStair->targetPos[Stair::RIGHT];
		moveDirection = 1;
		SendPlayerPos();
		break;
	case KEY_W:
		pos = stayStair->targetPos[Stair::UP];
		SendPlayerPos();
		break;
	case KEY_S:
		pos = stayStair->targetPos[Stair::DOWN];
		SendPlayerPos();
		break;
	}
}

Player* PlayersManager::FindNearestPlayer(vec2 point, float maxDistance, Player* ignore) {
	float min = maxDistance;
	Player* p = nullptr;
	for (size_t i = 0; i < players.size(); i++) {
		if (players[i] == ignore)
			continue;
		const float distance = length(players[i]->pos - point);
		if (distance < min) {
			min = distance;
			p = players[i];
		}
	}
	return p;
}

int Player::totalPlayerCnt = 0;
vector<Player*> PlayersManager::players;