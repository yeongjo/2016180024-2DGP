#include "stdafx.h"
#include "Player.h"

bool Player::PlayerScore::Update() {
	if (score >= 100) { return true; }
	score += increaseScoreAmount;
	return false;
}

Player::Player(): Obj() {
	id = totalPlayerCnt++;
	PlayersManager::players.push_back(this);
	SetRandomPos();
	SendPlayerPos();
}

void Player::Update(float dt) {
	if (IsDead())
		return;

	if (IsMoving()) {
		speed = isRun ? runSpeed : walkSpeed;
		pos.x += speed * dt * (float)moveDirection;
		SendPlayerPos();
	}
}

bool Player::SetInput(ClientKeyInputPacket packet) {
	if (IsControlable() || id != packet.id) return false;
	if(stayStair) {
		MoveInStair(packet.key);
		return true;
	}
	auto value = packet.isDown ? 1 : -1;
	moveDirection += packet.key == KEY_A * value;
	moveDirection -= packet.key == KEY_D * value;
	lookDirec = moveDirection != 0 ? moveDirection : lookDirec;
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
	attackPos.y += 50;
	auto player = PlayersManager::FindNearestPlayer(attackPos, 150);
	if(player != nullptr) {
		// TODO 본인 ID와 foundId를 모든 클라에게 전송
		player->TakeDamage(1);
	}
}

void Player::Interact() {
	auto interactedObjId = InteractObjManager::Interact(this);
	if (interactedObjId != -1) {
		//TODO id 와 interactedObjId 를 클라들에게 보낸다.
	}
}

void Player::SetRandomPos() {
	pos.x = Random(0, 2) * 1920;
	pos.y = Building::CalculateFloorHeight(Random(0, 6));
}

bool Player::IsMoving() {
	return moveDirection != 0;
}

void Player::SendPlayerPos() {
	//TODO 모든 클라이언트에게 이동된 위치 전송
}

bool Player::IsControlable() {
	return !IsDead() && !stayStair;
}

void Player::MoveInStair(int key) {
	switch (key) {
	case KEY_A:
		if(stayStair->otherStairs[Stair::LEFT])
		pos = stayStair->otherStairs[Stair::LEFT]->pos;
		break;
	case KEY_D:
		if (stayStair->otherStairs[Stair::RIGHT])
		pos = stayStair->otherStairs[Stair::RIGHT]->pos;
		break;
	case KEY_W:
		if (stayStair->otherStairs[Stair::UP])
		pos = stayStair->otherStairs[Stair::UP]->pos;
		break;
	case KEY_S:
		if (stayStair->otherStairs[Stair::DOWN])
		pos = stayStair->otherStairs[Stair::DOWN]->pos;
		break;
	}
}

Player* PlayersManager::FindNearestPlayer(vec2 point, float maxDistance) {
	float min = maxDistance;
	Player* p = nullptr;
	for (size_t i = 0; i < players.size(); i++) {
		const float distance = (players[i]->pos - point).length();
		if (distance < min) {
			min = distance;
			p = players[i];
		}
	}
	return p;
}

int Player::totalPlayerCnt = 0;
vector<Player*> PlayersManager::players;