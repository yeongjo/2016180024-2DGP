#pragma once
#include "Building.h"
#include "Packets.h"

class Player : public Obj {
	struct PlayerScore {
		int score = 0;
		int increaseScoreAmount = 0; // Ȱ��ȭ�� ���� ���� ���

		// ���ӿ��� �̰�ٸ� true
		bool Update();
	};

public:
	PlayerScore score;

	Player();

	void Update(float dt);

	bool SetInput(ClientKeyInputPacket packet); // �Է���Ŷ ����

	void TakeDamage(int damage);

	bool IsDead() const;

private:
	void Attack();

	void Interact();

	void SetRandomPos();

	bool IsMoving();

	void SendPlayerPos();

	int health = 2;
	static constexpr float walkSpeed = 300;
	static constexpr float runSpeed = 300 * 1.8f;
	float speed = walkSpeed;
	bool isInStair = false;
	ClientKeyInputPacket lastInput;
	int moveDirection = 0;
	bool isAttack = false;
	bool isRun = false;
	bool isInteract = false;

	static int totalPlayerCnt;
};

class PlayersManager {
public:
	static vector<Player*> players;

	// �÷��̾� ID ��ȯ, ���н� -1 ��ȯ
	static int FindNearestPlayer(vec2 point, float maxDistance);
};