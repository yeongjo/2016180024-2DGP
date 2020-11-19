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
	if (id != packet.id) return false;
	lastInput = packet;
	auto value = lastInput.isDown ? 1 : -1;
	moveDirection += lastInput.id == KEY_A * value;
	moveDirection -= lastInput.id == KEY_D * value;
	switch (lastInput.id) {
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
	auto foundId = PlayersManager::FindNearestPlayer(pos, 150);
	if(foundId != -1) {
		// TODO ���� ID�� foundId�� ��� Ŭ�󿡰� ����
	}
}

void Player::Interact() {
	auto interactedObjId = InteractObjManager::Interact(this);
	if (interactedObjId != -1) {
		//TODO id �� interactedObjId �� Ŭ��鿡�� ������.
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
	//TODO ��� Ŭ���̾�Ʈ���� �̵��� ��ġ ����
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