#include "stdafx.h"
#include "Player.h"

int playerCount = 0;

bool Player::PlayerScore::Update() {
	if (score >= 100) { return true; }
	score += increaseScoreAmount;
	return false;
}

Player::Player(): Obj() {
	id = totalPlayerCnt++;
	PlayersManager::players.push_back(this);
	SetRandomPos();
}

void Player::Update(float dt) {
	if (IsDead())
		return;

	if (lastInput.isAttack)
		Attack();

	if (lastInput.isInteraction)
		Interact();

	if (IsMoving()) {
		speed = lastInput.isRun ? runSpeed : walkSpeed;
		pos.x += speed * dt * (float)lastInput.moveDirection;
		SendPlayerPos();
	}
}

bool Player::SetInput(ClientKeyInputPacket packet) {
	if (id != packet.id) return false;
	lastInput = packet;

	return true;
}

void Player::TakeDamage(int damage) {
	health -= damage;
}

bool Player::IsDead() const {
	return health <= 0;
}

void Player::Attack() {
	lastInput.isAttack = false;
	auto foundId = PlayersManager::FindNearestPlayer(pos, 150);
	if(foundId != -1) {
		// TODO 본인 ID와 foundId를 모든 클라에게 전송
	}
}

void Player::Interact() {
	lastInput.isInteraction = false;
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
	return lastInput.moveDirection != 0;
}

void Player::SendPlayerPos() {
	//TODO 모든 클라이언트에게 이동된 위치 전송
}

int PlayersManager::FindNearestPlayer(vec2 point, float maxDistance) {
	float min = maxDistance;
	int foundId = -1;
	for (size_t i = 0; i < players.size(); i++) {
		const float distance = (players[i]->pos - point).length();
		if (distance < min) {
			min = distance;
			foundId = i;
		}
	}
	return foundId;
}

int Player::totalPlayerCnt = 0;
vector<Player*> PlayersManager::players;