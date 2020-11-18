#pragma once

class Timer {
	class DelayC {
		int remainTime;
		int _remainTime = 0;
		bool isLoop;
		bool isBreak = false;

	public:
		int idx = 0;

		DelayC(int _remain, bool _isLoop, bool beginStart, int id);

		bool Tick(int add = 1);

		void SetEnd();

		void SetRemainTime(int _remain, bool _isLoop);

		void ChangeRemainTime(int time);

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
	static int Create(int _remainTime, bool _isLoop = false, bool beginStart = true);

	// input custom ID
	static int Create(int _remainTime, int _id, bool _isLoop = false, bool beginStart = true);

	// must call this on other tick
	static void Tick(int add = 1);

	static bool IsEnd(int idx);

	static void SetEnd(int idx);

	static void ChangeEndTime(int idx, int time);

	static void Reset(int idx);

	static void EndNext(int idx);

	static bool IsHere(int idx);

	static void Debug();
};
