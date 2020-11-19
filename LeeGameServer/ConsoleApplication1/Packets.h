#pragma once
#include "stdafx.h"

class IJsonSerializable;

enum class EPacketType {
	Error = -1,
	Player,
	Interact,
	ClientKeyInput,
	Score,
	WinPlayerId,
	MapData,
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
	int moveDirection = 0;
	bool isInteraction = false;
	bool isRun = false;
	bool isAttack = false;

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
	int winPlayerId = -1; // �̱� �÷��̾��� id

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};

class MapDataPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::MapData;
	vector<vec2> furniturePos; // ���� ��ġ

	void Serialize(Json::Value& root);

	void Deserialize(Json::Value& root);
};