#pragma once
#include "stdafx.h"

class IJsonSerializable;

#define KEY_A 97
#define	KEY_D 100
#define	KEY_S 115
#define	KEY_W 119
#define	KEY_H 104
#define	KEY_J 106
#define	KEY_K 107
#define	KEY_2 50


enum class EPacketType {
	Error = -1,
	Player,
	Interact,
	ClientKeyInput,
	Score,
	WinPlayerId,
	MapData,
	PlayerID,
};

class CJsonSerializer
{
public:
	static bool Serialize(IJsonSerializable* pObj, std::string& output);
	static bool Deserialize(IJsonSerializable* pObj, std::string& input);

private:
	CJsonSerializer();
};

class IJsonSerializable {
public:
	virtual ~IJsonSerializable();
	virtual void Serialize(Json::Value& root) = 0;
	virtual void Deserialize(Json::Value& root) = 0;
};

class PlayerPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::Player;
	int id = -1;
	glm::vec2 pos = glm::vec2(0, 0);

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};

class InteractPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::Interact;
	int interactPlayerId = 0;
	int interactedObjId = 0;

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};

class ClientKeyInputPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::ClientKeyInput;
	int id = -1;
	int key = 0;
	bool isDown = false;

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};

class ScorePacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::Score;
	vector<int> scores; // scores[playerCount]

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};

class WinPlayerIdPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::WinPlayerId;
	int winPlayerId = -1; // 이긴 플레이어의 id

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};

class MapDataPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::MapData;	
	vector<vec2> furniturePos; // 가구 위치

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};


class PlayerIdPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::PlayerID;
	int PlayerId = 0; // id

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};
