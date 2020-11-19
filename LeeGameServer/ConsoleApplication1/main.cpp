#include "stdafx.h"

#include "Building.h"
#include "GameManager.h"
#include "Packets.h"

DWORD WINAPI ProcessClient(LPVOID arg)
{
	SOCKET client_sock = (SOCKET)arg;
	unsigned int count;
	int retval;
	SOCKADDR_IN clientaddr;
	int addrlen = sizeof(clientaddr);
	char buf[BUFSIZE];	

	// 클라이언트 정보 얻기    
	getpeername(client_sock, (SOCKADDR*)&clientaddr, &addrlen);	
			
	retval = recv(client_sock, buf, BUFSIZE, 0);
	if (retval == SOCKET_ERROR) { err_display("recv() err 3"); }	

	char* tok2 = strtok(buf, "}");
	strcat(tok2, "}");
	cout << tok2 << endl;
	

	closesocket(client_sock);
	printf("\n[TCP 서버] 클라이언트 종료: IP 주소=%s, 포트번호=%d\n", inet_ntoa(clientaddr.sin_addr), ntohs(clientaddr.sin_port));

	return 0;
}

int main()
{
	GameManager gm;	
	int retval;
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		return 1;

	//socket
	SOCKET listen_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (listen_sock == INVALID_SOCKET) err_quit("socket() err");

	//bind
	SOCKADDR_IN serveraddr;
	ZeroMemory(&serveraddr, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serveraddr.sin_port = htons(SERVERPORT);
	retval = bind(listen_sock, (SOCKADDR*)&serveraddr, sizeof(serveraddr));
	if (retval == SOCKET_ERROR) err_quit("bind() err");

	// listen()
	retval = listen(listen_sock, SOMAXCONN);
	if (retval == SOCKET_ERROR) err_quit("listen()");

	// 데이터 통신에 사용할 변수
	SOCKET client_sock;
	SOCKADDR_IN clientaddr;
	int addrlen;
	vector<HANDLE> hThread;


	// 네트워크 접속 관련 추가되어야하는곳
	//...
	// 접속한 플레이어에게 순서대로 자신의 ID [0~..] 알려줘야함
	int playerCnt = 0; // 들어온 플레이어 수도 알려줘
	// 플레이어 들어옴
	// 클라이언트에게 playerCnt를 ID로 전송
	
	while (1)
	{
		//accept        
		addrlen = sizeof(clientaddr);
		client_sock = accept(listen_sock, (SOCKADDR*)&clientaddr, &addrlen);
		if (client_sock == INVALID_SOCKET) { err_display("accept() err"); break; }

		printf("\n[TCP 서버] 클라이언트 접속: IP 주소=%s, 포트번호=%d\n", inet_ntoa(clientaddr.sin_addr), ntohs(clientaddr.sin_port));
		// 스레드 생성        		
		hThread.push_back(CreateThread(NULL, 0, ProcessClient, (LPVOID)client_sock, 0, NULL));
		if (hThread[playerCnt] == NULL) { closesocket(client_sock); }
		else { CloseHandle(hThread[playerCnt]); }
		playerCnt++;
	}


	// 네트워크에 접속되고 나서 호출되어야함
	gm.Init(playerCnt);

	while(true) {
		gm.Update(0.016f);
		Sleep(16);
	}
	

	////c++ json 사용 예
	//MapDataPacket w;
	//w.furniturePos.push_back({ 1, 0 });
	//w.furniturePos.push_back({ 12, 03 });
	//string s;
	//CJsonSerializer::Serialize(&w, s);
	//cout << s;

	//MapDataPacket w2;
	//CJsonSerializer::Deserialize(&w2, s);
	//cout << endl;
	//cout << w2.furniturePos[0][0] <<" "  << w2.furniturePos[0][1] << endl;	//1  0
	//cout << w2.furniturePos[1][0] << " " << w2.furniturePos[1][1] << endl;	//12 3
	closesocket(listen_sock);
	WSACleanup();
}