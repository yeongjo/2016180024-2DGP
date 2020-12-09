#include "stdafx.h"
#include "NetworkManager.h"

#include "GameManager.h"

vector<SOCKET> client_sock;
int playerCnt = 0;
bool startToCloseClients = false;

int getPlayerCnt()
{
	return playerCnt;
}

void setPlayerCnt(int cnt) {
	playerCnt = cnt;
}

DWORD WINAPI ProcessClient(LPVOID arg)
{
	SOCKET client_sock = (SOCKET)arg;
	unsigned int count;
	int retval;
	SOCKADDR_IN clientaddr;
	int addrlen = sizeof(clientaddr);
	char buf[RECVBUFSIZE];

	// Ŭ���̾�Ʈ ���� ���    
	getpeername(client_sock, (SOCKADDR*)&clientaddr, &addrlen);

	ClientKeyInputPacket input;
	Json::CharReaderBuilder b;
	Json::CharReader* reader(b.newCharReader());
	std::string errs;
	Json::Value root;

	cout << "���� ������ �÷��̾� id: " << playerCnt << endl;
	SendPlayerIDPacketToClients(playerCnt++);
	
	//Ŭ�� ƨ�ܵ� ������ ���Ͽɼ� ����
	BOOL optval = TRUE;
	setsockopt(client_sock, SOL_SOCKET, SO_KEEPALIVE, (char*)&optval, sizeof(optval));

	

	while (!startToCloseClients)
	{
		if (!optval)
			cout << "�����׾���" << endl;
		//recv
		retval = recv(client_sock, buf, RECVBUFSIZE, 0);
		if (retval == SOCKET_ERROR) {
			cout << "recv ����� Ŭ���̾�Ʈ �����..\n";
			return 0;
		}
		//cout << "recv msg " << retval << endl;
		if(retval == 0) {
			Sleep(1);
			continue;
		}		
		string packet = strtok(buf, "}");
		packet += "}";

		//Parsing
		reader->parse(packet.c_str(), packet.c_str() + packet.length(), &root, &errs);
		input.Deserialize(root);
		cout << "key : " << input.key << "\t ID : " << input.id << "\t isDown : " << input.isDown << endl;
		GameManager::Self()->UpdatePlayerInput(input);
		//Sleep(16);
	}

	closesocket(client_sock);
	printf("\n[TCP ����] Ŭ���̾�Ʈ ����: IP �ּ�=%s, ��Ʈ��ȣ=%d\n", inet_ntoa(clientaddr.sin_addr), ntohs(clientaddr.sin_port));

	return 0;
}

void SendPlayerIDPacketToClients(int id)
{
	PlayerIdPacket pID;
	pID.type = EPacketType::PlayerID;	
	pID.PlayerId = id;
	int retval;
	string s;
	CJsonSerializer::Serialize(&pID, s);

	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { cout << ("SendPlayerIDPacketToClients() err 3"); std::cout << endl; }
	}
}

void SendMapDataPackets(MapDataPacket mapData) {	
	mapData.type = EPacketType::MapData;		
	int retval;
	string s;
	CJsonSerializer::Serialize(&mapData, s);
	std::cout << "�ʵ����� ���� : " << s << endl;

	for (int client = 0; client < client_sock.size(); client++) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		if (retval == SOCKET_ERROR) { cout << ("SendMapDataPackets err"); std::cout << endl; }
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
		if (retval == SOCKET_ERROR) { cout << ("SendChangedPlayerPositionToClients() err"); std::cout << endl; }
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
		if (retval == SOCKET_ERROR) { cout << ("SendInteractPacketToClients() err"); std::cout << endl; }
	}	
}

void SendPlayersScoreToClients(ScorePacket score)
{
	score.type = EPacketType::Score;
	int retval;
	string s;
	CJsonSerializer::Serialize(&score, s);

	for (int client = 0; client < client_sock.size(); ) {
		retval = send(client_sock[client], s.c_str(), BUFSIZE, 0);
		//��Ӻ�����ģ���� �ȹ����� ������
		if (retval == SOCKET_ERROR) {
			closesocket(client_sock[client]);
			client_sock.erase(client_sock.begin() + client);
			cout << "SendPlayersScoreToClients() exception " << "idx: "<< client << " " << client_sock.size() << " " << GameManager::Self()->players.size();
			if (client_sock.size()+1 == GameManager::Self()->players.size()) {
				cout << " ���� �÷��̾� id: " << GameManager::Self()->players[client]->id;
				GameManager::Self()->KillPlayer(client);
			}
			cout << endl;
		}else {
			client++;
		}
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
		if (retval == SOCKET_ERROR) { cout << ("SendWinPlayerIdPacketToClients err"); std::cout << endl; }
	}
}

vector<HANDLE> hThread;
DWORD WINAPI JoinPlayerThread(LPVOID arg) {
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


	//send socket
	SOCKET send_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (send_sock == INVALID_SOCKET) err_quit("socket() err ������ ������");

	// ��Ʈ��ũ ���� ���� �߰��Ǿ���ϴ°�
	//...
	// ������ �÷��̾�� ������� �ڽ��� ID [0~..] �˷������

	// �÷��̾� ����
	// Ŭ���̾�Ʈ���� playerCnt�� ID�� ����
	std::cout << "���� ����" << endl;
	
	while (true)
	{		
		//accept        
		addrlen = sizeof(clientaddr);
		client_sock.push_back(accept(listen_sock, (SOCKADDR*)&clientaddr, &addrlen));
		int lastIdx = client_sock.size()-1;
		//#client_sock = accept(listen_sock, (SOCKADDR*)&clientaddr, &addrlen);
		if (client_sock[lastIdx] == INVALID_SOCKET) { err_display("accept() err"); break; }
		std::printf("\n[TCP ����] Ŭ���̾�Ʈ ����: IP �ּ�=%s, ��Ʈ��ȣ=%d\n", inet_ntoa(clientaddr.sin_addr), ntohs(clientaddr.sin_port));
		// ������ ����        		
		hThread.push_back(CreateThread(NULL, 0, ProcessClient, (LPVOID)client_sock[lastIdx], 0, NULL));
		int threadLastIdx = hThread.size() - 1;
		if (hThread[threadLastIdx] == NULL) { closesocket(client_sock[lastIdx]); } else { CloseHandle(hThread[threadLastIdx]); }
	}
}

void CloseAllClients() {
	// TODO vector push�� clear�� ���ÿ� �Ͼ�� ������������
	//startToCloseClients = true;

	//// �����尡 ���� ����Ǳ� ��ٸ���.
	//while(1) {

	//	Sleep(100);
	//}
	//
	//for (int i = 0; i < hThread.size(); i++)
	//{
	//	CloseHandle(hThread[i]);
	//}
	for (int i = 0; i < client_sock.size(); i++)
	{
		closesocket(client_sock[i]);
	}
	client_sock.resize(0);
	hThread.resize(0);

	//startToCloseClients = false;
	playerCnt = 0;
}

int InitServerSocket()
{
	CreateThread(NULL, 0, JoinPlayerThread, (LPVOID)NULL, 0, NULL);

	

	//PlayerPacket test;	

	//for (size_t j = 0; j < 10; j++)
	//{
	//	for (int i = 0; i < client_sock.size(); i++) {
	//		test.id = i;
	//		test.pos = vec2(1, j);
	//		SendChangedPlayerPositionToClients(test);
	//	}
	//	Sleep(16);
	//}


	/*closesocket(listen_sock);
	WSACleanup();*/
	return 0;
}