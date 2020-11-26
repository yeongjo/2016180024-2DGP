#include "stdafx.h"
#include "Building.h"

#include "NetworkManager.h"
#include "Player.h"

#define STAIR_CHECK_DISTANCE 50

int InteractObj::totalObjCnt = 100;

InteractObj::InteractObj() {
	id = totalObjCnt++;
	InteractObjManager::interactObjs.push_back(this);
}

int InteractObj::Interact(Obj* other) {
	if (length(pos - other->pos) <= interactDistance) {
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

Stair::Stair(vec2 pos) {
	this->pos = pos;
	targetPos.resize(4);
	for (int i = 0; i < 4; ++i)
		targetPos[i] = pos;
}

void Stair::SetTargetPos(vec2 other, int idx) {
	targetPos[idx] = other;
}

void Furniture::OnInteracted(Obj* other) {
	if (interactPlayer) {
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
	vec2 buildingPos[] = { {0, MAP_HEIGHT}, {MAP_WIDTH - 1, MAP_HEIGHT}, {0, 0}, {MAP_WIDTH - 1, 0} };

	float stairPosX[] = { 649, 540 };
	stairs.resize(6);
	for (int i = 0; i < 4; i++) {
		int is_right = i % 2;
		int j = 0;
		// 건물 왼쪽 계단
		for (auto y : EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING) {
			auto tStairPos = vec2(-stairPosX[0] + 18 * is_right + buildingPos[i].x, y + buildingPos[i].y);
			stairs[i / 2 * 3 + j].push_back({ tStairPos });
			++j;
		}
		j = 0;
		// 건물 오른쪽 계단
		for (auto y : EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING) {
			auto tStairPos = vec2(stairPosX[1] + 18 * is_right + buildingPos[i].x, y + buildingPos[i].y);
			stairs[i / 2 * 3 + j].push_back({ tStairPos });
			++j;
		}
	}

	for (int i = 0; i < 6; i++) {
		stairs[i][1].SetTargetPos(stairs[i][1].pos + vec2(-(STAIR_CHECK_DISTANCE+50), 0), Stair::LEFT);
		stairs[i][1].SetTargetPos(stairs[i][2].pos, Stair::RIGHT);
		stairs[i][2].SetTargetPos(stairs[i][2].pos + vec2((STAIR_CHECK_DISTANCE + 50), 0), Stair::RIGHT);
		stairs[i][2].SetTargetPos(stairs[i][1].pos, Stair::LEFT);

		stairs[i][0].SetTargetPos(stairs[i][0].pos + vec2((STAIR_CHECK_DISTANCE + 50), 0), Stair::RIGHT);
		stairs[i][3].SetTargetPos(stairs[i][3].pos - vec2((STAIR_CHECK_DISTANCE + 50), 0), Stair::LEFT);
	}
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 4; j++) {
			stairs[i][j].SetTargetPos(stairs[i + 1][j].pos, Stair::DOWN);
			stairs[i + 1][j].SetTargetPos(stairs[i][j].pos, Stair::UP);
		}
	}
}

void Building::CreateFurnitures() {
	for (size_t x = 0; x < 2; x++) {
		for (size_t y = 0; y < 6; y++) {
			float startX = x * (MAP_WIDTH - MAP_HALF_WIDTH);
			float i = WALLSIZE + startX;
			float endX = MAP_WIDTH - WALLSIZE + startX;
			while (i < endX - 300) {
				float random_x = i;
				float floorHeight = CalculateFloorHeight(y);
				auto furniture = new Furniture();
				furniture->pos.x = random_x + (FurnitureImgWidth / 2);
				furniture->pos.y = floorHeight;
				furnitures.push_back(furniture);
				i += FurnitureImgWidth / 2 + Random(100, 400);
			}
		}
	}
	MapDataPacket mapData;
	for (int i = 0; i < furnitures.size(); i++) {
		mapData.furniturePos.push_back(furnitures[i]->pos);
	}
	cout << "만들어진 가구 수 : " << furnitures.size() << endl;
	SendMapDataPackets(mapData);
}

Stair* Building::IsInStair(vec2 pos) {
	for(auto& a : stairs) {
		for(auto& b : a) {
			if(length(b.pos - pos) < STAIR_CHECK_DISTANCE) {
				return &b;
			}
		}
	}
	return nullptr;
}

// 0~5층까지
float Building::CalculateFloorHeight(int floor) {
	return floor >= 3
		? EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT
		: EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor];
}
