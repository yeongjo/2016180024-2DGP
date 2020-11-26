#pragma once
#include "stdafx.h"


#include "Building.h"
#include "Building.h"

#define MAP_WIDTH 1920
#define MAP_HEIGHT 1080
#define MAP_HALF_WIDTH (MAP_WIDTH/2)
#define MAP_HALF_HEIGHT (MAP_HEIGHT/2)
#define WALLSIZE 400
#define FurnitureImgWidth 50

class Player;

class Obj {
public:
	int id = -1;
	vec2 pos = vec2(0, 0);

	Obj() {
	}
	virtual ~Obj(){}
};

class InteractObj : public Obj
{
	float interactDistance = 150;
	static int totalObjCnt;
protected:
	virtual void OnInteracted(Obj* other) = 0;
public:
	InteractObj();
	int Interact(Obj* other);
};

class InteractObjManager {
public:
	static vector<InteractObj*> interactObjs;

	static int Interact(Obj* other);
};

class Stair : public Obj {
public:
	static constexpr int UP = 0;
	static constexpr int DOWN = 1;
	static constexpr int LEFT = 2;
	static constexpr int RIGHT = 3;
	vector<vec2> targetPos; // ��� �ǹ��� �´������ ���� ����� ��� ������

	Stair(vec2 pos);

	void SetTargetPos(vec2 other, int idx);
};

class Furniture : public InteractObj {
protected:
	// ��ȣ�ۿ� �� �÷��̾�� ���� �߰��� ��
	void OnInteracted(Obj* other) override;
public:
	Player* interactPlayer = nullptr;
};

class Building
{
	static constexpr float EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[3] = { 218, -139, -500 };

public:
	vector<vector<Stair>> stairs;
	vector<Furniture*> furnitures;

	void Init();
	
	Stair* IsInStair(vec2 pos);

	// �� ���� �ٴ��� ���̰� ������ �޴� �Լ�
	static float CalculateFloorHeight(int floor);
private:
	// ��ܰ� �浹�˻縦 ���� ��� ����
	void CreateStairs();

	void CreateFurnitures();

};

