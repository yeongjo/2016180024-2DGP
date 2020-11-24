#include "stdafx.h"
#include "NetworkManager.h"
#include "Building.h"
#include "GameManager.h"

int main()
{	
	GameManager gm;	
	setlocale(LC_ALL, "korean");

	InitServerSocket();

	int playerCnt = 2; //?
	// 네트워크에 접속되고 나서 호출되어야함
	gm.Init(playerCnt);

	while(true) {
		gm.Update(0.016f);
		Sleep(16);
	}	

}