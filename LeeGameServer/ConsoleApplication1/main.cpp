#include "stdafx.h"

#include "Building.h"
#include "GameManager.h"
#include "Packets.h"

int main()
{
	GameManager gm;

	// 네트워크 접속 관련 추가되어야하는곳
	//...
	// 접속한 플레이어에게 순서대로 자신의 ID [0~..] 알려줘야함
	int playerCnt = 0; // 들어온 플레이어 수도 알려줘
	// 플레이어 들어옴
	// 클라이언트에게 playerCnt를 ID로 전송
	playerCnt++;


	// 네트워크에 접속되고 나서 호출되어야함
	gm.Init(playerCnt);

	while(true) {
		gm.Update(0.016f);
		Sleep(16);
	}

	//c++ json 사용 예
	//MapDataPacket w;
	//w.furniturePos.push_back({ 1, 0 });
	//w.furniturePos.push_back({ 12, 03 });
	//string s;
	//CJsonSerializer::Serialize(&w, s);
	//cout << s;

	//MapDataPacket w2;
	//CJsonSerializer::Deserialize(&w2, s);
	//cout << endl;
}