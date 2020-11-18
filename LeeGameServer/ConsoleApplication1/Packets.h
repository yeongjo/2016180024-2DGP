#pragma once
#include "stdafx.h"

class IJsonSerializable;

int playerCount = 0;

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
	CJsonSerializer() {}
};

class IJsonSerializable {
public:
	virtual ~IJsonSerializable() {}
	virtual void Serialize(Json::Value& root) = 0;
	virtual void Deserialize(Json::Value& root) = 0;
};

class PlayerPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::Player;
	int id = -1;
	glm::vec2 pos = glm::vec2(0, 0);

	void Serialize(Json::Value& root) {
		root["type"] = (int)type;
		root["id"] = id;
		root["posx"] = pos.x;
		root["posy"] = pos.y;
	}
	void Deserialize(Json::Value& root) {
		type = (EPacketType)root.get("type", -1).asInt();
		id = root.get("id", -1).asInt();
		pos.x = root.get("posx", 0.0).asFloat();
		pos.y = root.get("posy", 0.0).asFloat();
	}
};

class InteractPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::Interact;
	int interactPlayerId = 0;
	int interactedObjId = 0;

	void Serialize(Json::Value& root) {
		root["type"] = (int)type;
		root["interactPlayerId"] = interactPlayerId;
		root["interactedObjId"] = interactedObjId;
	}
	void Deserialize(Json::Value& root) {
		type = (EPacketType)root.get("type", -1).asInt();
		interactPlayerId = root.get("interactPlayerId", -1).asInt();
		interactedObjId = root.get("interactedObjId", -1).asInt();
	}
};

class ClientKeyInputPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::ClientKeyInput;
	int id = -1;
	int moveDirection = 0;
	bool isInteraction = false;
	bool isRun = false;
	bool isAttack = false;

	void Serialize(Json::Value& root) {
		root["type"] = (int)type;
		root["moveDirection"] = moveDirection;
		root["id"] = id;
		root["isInteraction"] = isInteraction;
		root["isRun"] = isRun;
		root["isAttack"] = isAttack;
	}
	void Deserialize(Json::Value& root) {
		type = (EPacketType)root.get("type", -1).asInt();
		moveDirection = root.get("moveDirection", -1).asInt();
		id = root.get("id", -1).asInt();
		isAttack = root.get("isAttack", -1).asBool();
		isRun = root.get("isRun", -1).asBool();
		isInteraction = root.get("isInteraction", -1).asBool();
	}
};

class ScorePacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::Score;
	vector<int> scores; // scores[playerCount]

	void Serialize(Json::Value& root) {
		root["type"] = (int)type;
		for (auto a : scores)
			root["scores"].append(a);
	}
	void Deserialize(Json::Value& root) {
		type = (EPacketType)root.get("type", -1).asInt();
		auto size = root.get("scores", -1).size();
		for (int i = 0; i < size; i++) {
			scores.push_back(root.get("scores", -1)[i].asInt());
		}
	}
};

class WinPlayerIdPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::WinPlayerId;
	int winPlayerId = -1; // 이긴 플레이어의 id

	void Serialize(Json::Value& root) {
		root["type"] = (int)type;
		root["winPlayerId"] = winPlayerId;
	}
	void Deserialize(Json::Value& root) {
		type = (EPacketType)root.get("type", -1).asInt();
		winPlayerId = root.get("winPlayerId", -1).asInt();
	}
};

class MapDataPacket : public IJsonSerializable {
public:
	EPacketType type = EPacketType::MapData;
	vector<vec2> furniturePos; // 이긴 플레이어의 id

	void Serialize(Json::Value& root) {
		root["type"] = (int)type;
		for (auto a : furniturePos) {
			root["furniturePosX"].append(a.x);
			root["furniturePosY"].append(a.y);
		}
	}
	void Deserialize(Json::Value& root) {
		type = (EPacketType)root.get("type", -1).asInt();
		auto size = root.get("furniturePosX", -1).size();
		for (int i = 0; i < size; i++) {
			auto x = root.get("furniturePosX", 0)[i].asFloat();
			auto y = root.get("furniturePosY", 0)[i].asFloat();
			furniturePos.push_back({x,y});
		}
	}
};

bool CJsonSerializer::Serialize(IJsonSerializable* pObj, std::string& output)
{
	if (pObj == NULL)
		return false;

	Json::Value serializeRoot;
	pObj->Serialize(serializeRoot);

	stringstream ss;
	Json::StreamWriterBuilder streamWriter;
	std::unique_ptr<Json::StreamWriter> writer(
		streamWriter.newStreamWriter());
	writer->write(serializeRoot, &ss);
	output = ss.str();

	return true;
}

bool CJsonSerializer::Deserialize(IJsonSerializable* pObj, std::string& input)
{
	if (pObj == NULL)
		return false;

	JSONCPP_STRING errs;
	Json::Value deserializeRoot;
	Json::CharReaderBuilder builder;
	stringstream ss(input);
	bool ok = parseFromStream(builder, ss, &deserializeRoot, &errs);
	if (!ok) return false;

	pObj->Deserialize(deserializeRoot);

	return true;
}
