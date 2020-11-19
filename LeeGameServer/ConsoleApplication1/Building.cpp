#include "stdafx.h"
#include "Building.h"
#include "Player.h"

int Obj::totalObjCnt = 100;

InteractObj::InteractObj() {
	InteractObjManager::interactObjs.push_back(this);
}

int InteractObj::Interact(Obj* other) {
	if((pos - other->pos).length() <= interactDistance) {
		OnInteracted(other);
		return id;
	}
	return -1;
}

int InteractObjManager::Interact(Obj* other) {
	for (auto a : interactObjs) {
		auto interactedObjId = a->Interact(other);
		if (interactedObjId != -1)
			return interactedObjId;
	}
	return -1;
}

vector<InteractObj*> InteractObjManager::interactObjs;

Stair::Stair(vec2 pos, Stair* other): otherStair(other) {
	this->pos = pos;
}

void Stair::SetOtherStair(Stair* other) {
	otherStair = other;
	other->otherStair = this;
}

void Furniture::OnInteracted(Obj* other) {
	if(interactPlayer) {
		interactPlayer->score.increaseScoreAmount--;
	}
	auto p = dynamic_cast<Player*>(other);
	interactPlayer = p;
	p->score.increaseScoreAmount++;
}

void Building::Init() {
	CreateStairs();
	CreateFurnitures();
}

void Building::CreateStairs() {
	vec2 buildingPos[] = {{0, MAP_HEIGHT}, {MAP_WIDTH - 1, MAP_HEIGHT}, {0, 0}, {MAP_WIDTH - 1, 0}};

	float stairPosX[] = {649, 540};

	for (int i = 0; i < 4; i++) {
		int is_right = i % 2;
		for (auto y : EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING) {
			auto tStairPos = vec2(-stairPosX[0] + 18 * is_right + buildingPos[i].x, y + buildingPos[i].y);
			stairs.push_back({tStairPos, nullptr});
		}
		for (auto y : EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING) {
			auto tStairPos = vec2(stairPosX[1] + 18 * is_right + buildingPos[i].x, y + buildingPos[i].y);
			stairs.push_back({tStairPos, nullptr});
		}
	}

	for (int i = 0; i < 3; i++) {
		stairs[i + 3].SetOtherStair(&stairs[i + 6]);
		stairs[i + 3 + 12].SetOtherStair(&stairs[i + 6 + 12]);
	}
}

void Building::CreateFurnitures() {
	for (size_t x = 0; x < 2; x++) // �翷����
	{
		for (size_t y = 0; y < 6; y++) // ���Ʒ���
		{
			float offset = x * MAP_WIDTH - MAP_HALF_WIDTH;
			float i = WALLSIZE + offset;
			float limit_x = MAP_WIDTH - WALLSIZE + offset;
			while (i < limit_x - 300) {
				float random_x = i;
				float floorHeight = CalculateFloorHeight(y);
				Furniture furniture;
				furniture.pos.x = random_x + (FurnitureImgWidth / 2);
				furniture.pos.y = floorHeight;
				furnitures.push_back(furniture);
				i += FurnitureImgWidth / 2 + Random(0, 200);
			}
		}
	}
}

// 0~5층까지
float Building::CalculateFloorHeight(int floor) {
	return floor >= 3
		       ? EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT
		       : EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor];
}
