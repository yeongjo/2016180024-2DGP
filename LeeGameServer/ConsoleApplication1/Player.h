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

	virtual ~Player();

	void Update(float dt);

	bool SetInput(ClientKeyInputPacket packet); // �Է���Ŷ ����

	void TakeDamage(int damage);

	bool IsDead() const;

	void SendPlayerPos();

	void Suicide();

	bool UpdateScore();

	static int GetTotalPlayerCnt();

	static void Reset();
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
	int packetSendCnt = 2;
	int _packetSendCnt = 2;

	static int totalPlayerCnt;
};

class PlayersManager {
public:
	static vector<Player*> players;

	// �÷��̾� ID ��ȯ, ���н� -1 ��ȯ
	static Player* FindNearestPlayer(vec2 point, float maxDistance, Player* ignore = nullptr);
};