#pragma once
#include "stdafx.h"

#define MAP_WIDTH 1920
#define MAP_HEIGHT 1080
#define MAP_HALF_WIDTH MAP_WIDTH/2
#define MAP_HALF_HEIGHT MAP_HEIGHT/2
#define WALLSIZE 400
#define FurnitureImgWidth 50

class Player;

class Obj {
public:
	int id = -1;
	vec2 pos;

	Obj() {
		id = totalObjCnt++;
	}
	virtual ~Obj(){}
private:
	static int totalObjCnt;
};

class InteractObj : public Obj
{
	float interactDistance = 150;
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
	Stair* otherStair = nullptr; // ��� �ǹ��� �´������ ���� ����� ��� ������

	Stair(vec2 pos, Stair* other);

	void SetOtherStair(Stair* other);
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
	vector<Stair> stairs;
	vector<Furniture> furnitures;

	void Init();

	// �� ���� �ٴ��� ���̰� ������ �޴� �Լ�
	static float CalculateFloorHeight(int floor);
private:
	// ��ܰ� �浹�˻縦 ���� ��� ����
	void CreateStairs();

	void CreateFurnitures();
};

