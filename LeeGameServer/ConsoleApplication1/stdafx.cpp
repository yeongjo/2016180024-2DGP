#include "stdafx.h"

void print(LPCTSTR pszStr, ...) {
#ifdef _DEBUG
	TCHAR szMsg[256];
	va_list args;
	va_start(args, pszStr);
	_vstprintf_s(szMsg, 256, pszStr, args);
	OutputDebugString(szMsg);
#endif   
}