#include "stdafx.h"
#include "NetworkManager.h"
#include "Building.h"
#include "GameManager.h"

int main()
{	
	GameManager gm;	
	setlocale(LC_ALL, "korean");

	InitServerSocket();
		
	// 네트워크에 접속되고 나서 호출되어야함
	gm.Init();

	while(true) {
		gm.Update(0.016f);
		Sleep(16);
	}	

}