#pragma once

class Timer {
	class DelayC {
		float remainTime;
		float _remainTime = 0;
		bool isLoop;
		bool isBreak = false;

	public:
		int idx = 0;

		DelayC(float _remain, bool _isLoop, bool beginStart, int id);

		bool Tick(float add = 1);

		void SetEnd();

		void SetRemainTime(float _remain, bool _isLoop);

		void ChangeRemainTime(float time);

		bool IsEnd();

		void DebugRemainTime();

		void Reset();

		void EndNext();
	};
	
	static vector<DelayC> managingObjs;
	static vector<DelayC>::iterator iter;
	static int id;
public:
	// First return id is 0
	static int Create(float _remainTime, bool _isLoop = false, bool beginStart = true);

	// input custom ID
	static int Create(float _remainTime, int _id, bool _isLoop = false, bool beginStart = true);

	// must call this on other tick
	static void Tick(float add = 1);

	static bool IsEnd(int idx);

	static void SetEnd(int idx);

	static void ChangeEndTime(int idx, float time);

	static void Reset(int idx);

	static void EndNext(int idx);

	static bool IsHere(int idx);

	static void Debug();
};
