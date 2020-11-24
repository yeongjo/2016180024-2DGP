#include "stdafx.h"
#include "NetworkManager.h"

// ������ ��ſ� ����� ����
vector<SOCKET> client_sock;


DWORD WINAPI ProcessClient(LPVOID arg)
{
	SOCKET client_sock = (SOCKET)arg;
	unsigned int count;
	int retval;
	SOCKADDR_IN clientaddr;
	int addrlen = sizeof(clientaddr);
	char buf[BUFSIZE];

	// Ŭ���̾�Ʈ ���� ���    
	getpeername(client_sock, (SOCKADDR*)&clientaddr, &addrlen);

	ClientKeyInputPacket input;
	Json::CharReaderBuilder b;
	Json::CharReader* reader(b.newCharReader());
	std::string errs;
	Json::Value root;

	while (1)
	{
		//recv
		retval = recv(client_sock, buf, BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { err_display("recv() err 3"); }
		string packet = strtok(buf, "}");
		packet += "}";

		//Parsing
		reader->parse(packet.c_str(), packet.c_str() + packet.length(), &root, &errs);
		input.Deserialize(root);
		std::cout << "key : " << input.key << "\t ID : " << input.id << "\t isDown : " << input.isDown << endl;
		Sleep(160);
	}

	closesocket(client_sock);
	std::printf("\n[TCP ����] Ŭ���̾�Ʈ ����: IP �ּ�=%s, ��Ʈ��ȣ=%d\n", inet_ntoa(clientaddr.sin_addr), ntohs(clientaddr.sin_port));

	return 0;
}


void SendMapDataPackets(MapDataPacket mapData) {	
	std::cout << "�ʵ����� ����" << endl;
	mapData.type = EPacketType::MapData;		
	int retval;
	string s;
	CJsonSerializer::Serialize(&mapData, s);
	
	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { err_display("recv() err 3"); std::cout << endl; }
	}	
}

void SendChangedPlayerPositionToClients(PlayerPacket player)
{
	player.type = EPacketType::Player;	
	int retval;
	string s;
	CJsonSerializer::Serialize(&player, s);

	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { err_display("recv() err 3"); std::cout << endl; }
	}	
}

void SendInteractPacketToClients(InteractPacket interact)
{
	interact.type = EPacketType::Interact;	
	int retval;
	string s;
	CJsonSerializer::Serialize(&interact, s);

	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { err_display("recv() err 3"); std::cout << endl; }
	}	
}

void SendPlayersScoreToClients(ScorePacket score)
{
	score.type = EPacketType::Score;
	int retval;
	string s;
	CJsonSerializer::Serialize(&score, s);

	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { err_display("recv() err 3"); std::cout << endl; }
	}
}

void SendWinPlayerIdPacketToClients(WinPlayerIdPacket winplayer)
{
	winplayer.type = EPacketType::WinPlayerId;
	int retval;
	string s;
	CJsonSerializer::Serialize(&winplayer, s);

	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { err_display("recv() err 3"); std::cout << endl; }
	}
}

int InitServerSocket()
{
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


	SOCKADDR_IN clientaddr;
	int addrlen;
	vector<HANDLE> hThread;
	int playerCnt = 0;


	//send socket
	SOCKET send_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (send_sock == INVALID_SOCKET) err_quit("socket() err");

	// ��Ʈ��ũ ���� ���� �߰��Ǿ���ϴ°�
	//...
	// ������ �÷��̾�� ������� �ڽ��� ID [0~..] �˷������

	// �÷��̾� ����
	// Ŭ���̾�Ʈ���� playerCnt�� ID�� ����
	std::cout << "���� ����" << endl;

	while (playerCnt < MAXPLAYER)
	{

		//accept        
		addrlen = sizeof(clientaddr);
		client_sock.push_back(accept(listen_sock, (SOCKADDR*)&clientaddr, &addrlen));
		//#client_sock = accept(listen_sock, (SOCKADDR*)&clientaddr, &addrlen);
		if (client_sock[playerCnt] == INVALID_SOCKET) { err_display("accept() err"); break; }

		std::printf("\n[TCP ����] Ŭ���̾�Ʈ ����: IP �ּ�=%s, ��Ʈ��ȣ=%d\n", inet_ntoa(clientaddr.sin_addr), ntohs(clientaddr.sin_port));
		// ������ ����        		
		hThread.push_back(CreateThread(NULL, 0, ProcessClient, (LPVOID)client_sock[playerCnt], 0, NULL));
		if (hThread[playerCnt] == NULL) { closesocket(client_sock[playerCnt]); }
		else { CloseHandle(hThread[playerCnt]); }
		playerCnt++;
	}

	PlayerPacket test;	

	for (size_t j = 0; j < 10; j++)
	{
		for (int i = 0; i < client_sock.size(); i++) {
			test.id = i;
			test.pos = vec2(1, j);
			SendChangedPlayerPositionToClients(test);
		}
		Sleep(160);
	}	

	std::cout << "�÷��̾� �� ����" << endl;


	/*closesocket(listen_sock);
	WSACleanup();*/
}