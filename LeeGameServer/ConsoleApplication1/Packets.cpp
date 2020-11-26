#include "stdafx.h"
#include "Packets.h"

bool CJsonSerializer::Serialize(IJsonSerializable* pObj, std::string& output) {
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

bool CJsonSerializer::Deserialize(IJsonSerializable* pObj, std::string& input) {
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

CJsonSerializer::CJsonSerializer() {
}

IJsonSerializable::~IJsonSerializable() {
}

void PlayerPacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	root["id"] = id;
	root["posx"] = pos.x;
	root["posy"] = pos.y;
}

void PlayerPacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	id = root.get("id", -1).asInt();
	pos.x = root.get("posx", 0.0).asFloat();
	pos.y = root.get("posy", 0.0).asFloat();
}

void InteractPacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	root["interactPlayerId"] = interactPlayerId;
	root["interactedObjId"] = interactedObjId;
}

void InteractPacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	interactPlayerId = root.get("interactPlayerId", -1).asInt();
	interactedObjId = root.get("interactedObjId", -1).asInt();
}

void ClientKeyInputPacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	root["key"] = key;
	root["id"] = id;
	root["isDown"] = isDown;
}

void ClientKeyInputPacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	key = root.get("key", 0).asInt();
	id = root.get("id", -1).asInt();
	isDown = root.get("isDown", false).asBool();
}

void ScorePacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	for (auto a : scores)
		root["scores"].append(a);
}

void ScorePacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	auto size = root.get("scores", -1).size();
	for (int i = 0; i < size; i++) {
		scores.push_back(root.get("scores", -1)[i].asInt());
	}
}

void WinPlayerIdPacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	root["winPlayerId"] = winPlayerId;
}

void WinPlayerIdPacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	winPlayerId = root.get("winPlayerId", -1).asInt();
}

void MapDataPacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	for (auto a : furniturePos) {
		root["furniturePosX"].append(a.x);
		root["furniturePosY"].append(a.y);
	}
}

void MapDataPacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	auto size = root.get("furniturePosX", -1).size();
	for (int i = 0; i < size; i++) {
		auto x = root.get("furniturePosX", 0)[i].asFloat();
		auto y = root.get("furniturePosY", 0)[i].asFloat();
		furniturePos.push_back({ x, y });
	}
}


void PlayerIdPacket::Serialize(Json::Value& root) {
	root["type"] = (int)type;
	root["PlayerId"] = PlayerId;
}

void PlayerIdPacket::Deserialize(Json::Value& root) {
	type = (EPacketType)root.get("type", -1).asInt();
	PlayerId = root.get("PlayerId", -1).asInt();
}