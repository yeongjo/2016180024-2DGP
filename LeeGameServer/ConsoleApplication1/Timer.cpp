#include "stdafx.h"
#include "Timer.h"

vector<Timer::DelayC> Timer::managingObjs;
vector<Timer::DelayC>::iterator Timer::iter;
int Timer::id;


Timer::DelayC::DelayC(float _remain, bool _isLoop, bool beginStart, int id) {
	SetRemainTime(_remain, _isLoop);
	idx = id;
	if (beginStart)
		_remainTime = remainTime + 1;
}

bool Timer::DelayC::Tick(float add) {
	_remainTime += add;
	return isBreak;
}

void Timer::DelayC::SetEnd() {
	isBreak = true;
}

void Timer::DelayC::SetRemainTime(float _remain, bool _isLoop) {
	remainTime = _remain;
	isLoop = _isLoop;
}

void Timer::DelayC::ChangeRemainTime(float time) {
	remainTime = time;
}

bool Timer::DelayC::IsEnd() {
	if (remainTime < _remainTime) {
		if (isLoop)
			_remainTime = 0;
		else
			isBreak = true;
		return true;
	}
	return false;
}

void Timer::DelayC::DebugRemainTime() {
#ifdef _MBCS
	stringstream ss;
#endif
#ifdef _UNICODE
	wstringstream ss;
#endif
	//ss << idx << _T(":") << _remainTime << _T("/") << remainTime;
	//TextOut(hdc, x, y, ss.str().c_str(), ss.str().size());
}

void Timer::DelayC::Reset() {
	_remainTime = 0;
}

void Timer::DelayC::EndNext() {
	_remainTime = remainTime + 1;
}

int Timer::Create(float _remainTime, bool _isLoop, bool beginStart) {
	managingObjs.push_back(Timer::DelayC(_remainTime, _isLoop, beginStart, id));
	return id++;
}

// input ID and use

int Timer::Create(float _remainTime, int _id, bool _isLoop, bool beginStart) {
	if (id < _id) return 0;
	managingObjs.push_back(Timer::DelayC(_remainTime, _isLoop, beginStart, _id));
	id = _id + 1;
	return 1;
}

// must call this on other tick

void Timer::Tick(float add) {
	int t = 0;
	for (iter = managingObjs.begin(); iter != managingObjs.end(); ++t) {
		if (iter->Tick(add)) {
			iter = managingObjs.erase(iter);
		}
		else
			++iter;
	}
}

bool Timer::IsEnd(int idx) {
	for (size_t i = 0; i < managingObjs.size(); i++) {
		if (managingObjs[i].idx == idx) {
			return managingObjs[i].IsEnd();
		}
	}
	return false;
}

void Timer::SetEnd(int idx) {
	for (size_t i = 0; i < managingObjs.size(); i++) {
		if (managingObjs[i].idx == idx) {
			return managingObjs[i].SetEnd();
		}
	}
}

void Timer::ChangeEndTime(int idx, float time) {
	for (size_t i = 0; i < managingObjs.size(); i++) {
		if (managingObjs[i].idx == idx) {
			return managingObjs[i].ChangeRemainTime(time);
		}
	}
}

void Timer::Reset(int idx) {
	for (size_t i = 0; i < managingObjs.size(); i++) {
		if (managingObjs[i].idx == idx) {
			return managingObjs[i].Reset();
		}
	}
}

void Timer::EndNext(int idx) {
	for (size_t i = 0; i < managingObjs.size(); i++) {
		if (managingObjs[i].idx == idx) {
			return managingObjs[i].EndNext();
		}
	}
}

bool Timer::IsHere(int idx) {
	for (size_t i = 0; i < managingObjs.size(); i++) {
		if (managingObjs[i].idx == idx) {
			return true;
		}
	}
	return false;
}

void Timer::Debug() {
	int textY = 0;
	for (size_t i = 0; i < managingObjs.size(); i++) {
		managingObjs[i].DebugRemainTime();
		textY += 15;
	}
}