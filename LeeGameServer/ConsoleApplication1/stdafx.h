#pragma once
#include <iostream>
#include <json/json.h>
#include <sstream>
#include "glm/vec2.hpp"
#include <vector>
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