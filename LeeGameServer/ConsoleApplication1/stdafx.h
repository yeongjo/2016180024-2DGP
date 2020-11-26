#pragma once
#define _WINSOCK_DEPRECATED_NO_WARNINGS // 최신 VC++ 컴파일 시 경고 방지
#define _CRT_SECURE_NO_WARNINGS
#pragma comment(lib, "ws2_32")
#include <iostream>
#include <json/json.h>
#include <sstream>
#include "glm/vec2.hpp"
#include "glm/gtx/norm.hpp"
#include <vector>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <tchar.h>


using namespace std;
using namespace glm;

// min ~ max-1
inline int Random(int min, int max) {
	return min + rand() % (max - min);
}

inline float Random() {
	return rand() / (float)RAND_MAX;
}

void print(LPCTSTR pszStr, ...);

#define DebugPrint(...) print(L"%s %s %d: ", __FILEW__, __FUNCTIONW__, __LINE__, __VA_ARGS__);


#define SERVERIP    "127.0.0.1"
#define SERVERPORT  9000
#define BUFSIZE     1000
#define MAXPLAYER   2

inline void err_quit(const char* msg)
{
    LPVOID lpMsgBuf;
    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM, NULL, WSAGetLastError(),
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPTSTR)&lpMsgBuf, 0, NULL);
    MessageBox(NULL, (LPCTSTR)lpMsgBuf, (LPCWSTR)msg, MB_ICONERROR);
    LocalFree(lpMsgBuf);
    exit(1);
}

inline void err_display(const char* msg)
{
    LPVOID lpMsgBuf;
    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
        NULL, WSAGetLastError(),
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPTSTR)&lpMsgBuf, 0, NULL);
    printf("[%s] %s", msg, (char*)lpMsgBuf);
    LocalFree(lpMsgBuf);
}