#pragma once
#include "Building.h"
#include "Building.h"
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

	void SendPlayerPos();
private:
	void Attack();

	void Interact();

	void SetRandomPos();

	bool IsMoving();


	bool IsControlable();

	Stair* isInStair();

	void MoveInStair(int key);

	
	int health = 2;
	static constexpr float walkSpeed = 300;
	static constexpr float runSpeed = 300 * 1.8f;
	float speed = walkSpeed;
	int moveDirection = 0;
	int lookDirec = 1;
	bool isRun = false;
	Stair* stayStair = nullptr;

	static int totalPlayerCnt;
};

class PlayersManager {
public:
	static vector<Player*> players;

	// �÷��̾� ID ��ȯ, ���н� -1 ��ȯ
	static Player* FindNearestPlayer(vec2 point, float maxDistance, Player* ignore = nullptr);
};