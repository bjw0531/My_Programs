#include <bits/stdc++.h>
#include <stdio.h>
#include <Windows.h>
#include <conio.h>
#include <stdlib.h>
#include <string>

#define MAPSIZE 19
#define UP 72
#define DOWN 80
#define LEFT 75
#define RIGHT 77
#define preARROWKEY 224
#define ENTER 13
#define CURSOR "\033[38;2;255;182;73m◆\033[48;2;166;96;56m\033[38;2;38;12;7m"

using namespace std;

// Map
// 0 = 빈칸
// 1 = 흑돌
// 2 = 백돌
int Map[MAPSIZE][MAPSIZE];
// Turn
// T = 흑
// F = 백
bool Turn = true;
// 마지막 ControlCursor에서 반환한 좌표를 기억할 변수
pair<int, int> lastCoord;

// 프로토타입
void PrintScreen();
void gotoxy(int x, int y);
bool CheckMapOver(int x, int y);
pair<int, int> ControlCursor(pair<int, int> coord);
void CursorView();
string returnMapShape(int x, int y);
void PutStone(int x, int y);
int Algorithm(int x, int y);
int Finish();

int main()
{
Initialize:
	// 초기 설정
	system("cls");
	fill(&Map[0][0], &Map[0][0] + MAPSIZE * MAPSIZE, 0);
	Turn = true;
	CursorView();
	lastCoord.first = 9;
	lastCoord.second = 9;

	while (1)
	{
		PrintScreen();
		lastCoord = ControlCursor(lastCoord);

		if (Algorithm(lastCoord.first, lastCoord.second) == 1)	break;
		Turn = !Turn;
	}
	gotoxy(0, MAPSIZE);
	if (Finish() == 1)	goto Initialize;
}

void PrintScreen()
{
	// ┏ ┳ ┐┣ ┼ ┤└ ┴ ┘ ─ │
	// ┏ ┳ ┓┣ ╋ ┫┗ ┻ ┛ ━ ┃
	gotoxy(0, 0);
	int x, y; // 맵에 값이 있으면 출력하기 위함

	printf("\033[48;2;166;96;56m\033[38;2;38;12;7m"); // 배경 텍스트 색
	printf("┌─");
	for (int i = MAPSIZE - 2; i--;)	printf("┬─");
	printf("┐ ");

	printf("\033[0m"); // 배경 텍스트 색 초기화
	cout << "    현재 차례 : " << [](bool Turn) {return (Turn == true) ? "흑" : "백"; }(Turn) << endl;
	printf("\033[48;2;166;96;56m\033[38;2;38;12;7m"); // 배경 텍스트 색

	for (int i = MAPSIZE - 2; i--;)
	{
		printf("├─");
		for (int j = MAPSIZE - 2; j--;)	printf("┼─");
		printf("┤ \n");
	}

	printf("└─");
	for (int i = MAPSIZE - 2; i--;)	printf("┴─");
	printf("┘ \n");

	for (int i = 0; i < MAPSIZE; i++)
	{
		for (int j = 0; j < MAPSIZE; j++)
		{
			switch (Map[i][j])
			{
			case 1:
				gotoxy(j, i);
				printf("●");
				break;
			case 2:
				gotoxy(j, i);
				printf("\033[38;2;255;255;255m"); // 텍스트 하얀색
				printf("●");
				printf("\033[48;2;166;96;56m\033[38;2;38;12;7m"); // 배경 텍스트 색
				break;
			}
		}
	}
}

void gotoxy(int x, int y)
{
	COORD Pos;
	Pos.X = x * 2; // x는 2배 해줘야 x,y 동일한 좌표
	Pos.Y = y;
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), Pos);
}

pair<int, int> ControlCursor(pair<int, int> coord)
{
	// 입력받은 좌표에서 시작
	int x, y;
	x = coord.first;
	y = coord.second;

	// 마지막 밟은 좌표 기억
	int lastX = coord.first, lastY = coord.second;
	gotoxy(x, y);
	printf(CURSOR);

	while (true)
	{
		int input = _getch();
		if (input == ENTER)
		{
			PutStone(x, y);
			PrintScreen();
			break;
		}

		else if (input == preARROWKEY)
		{
			input = _getch();
			// 전에 밟았던 곳 다시 출력
			switch (Map[lastY][lastX])
			{
			case 0:
				gotoxy(lastX + 1, lastY);
				cout << "\b \b\b";
				cout << returnMapShape(lastX, lastY);
				break;
			case 1:
				gotoxy(lastX, lastY);
				printf("\033[48;2;166;96;56m\033[38;2;38;12;7m"); // 배경 텍스트 색
				printf("●");
				break;
			case 2:
				gotoxy(lastX, lastY);
				printf("\033[38;2;255;255;255m"); // 텍스트 하얀색
				printf("●");
				printf("\033[48;2;166;96;56m\033[38;2;38;12;7m"); // 배경 텍스트 색
				break;
			}

			// 커서 이동
			switch (input)
			{
			case UP:
				if (CheckMapOver(x, y - 1) == false)	gotoxy(x, --y);
				else									gotoxy(x, y);

				printf(CURSOR);
				lastX = x;
				lastY = y;
				break;

			case DOWN:
				if (CheckMapOver(x, y + 1) == false)	gotoxy(x, ++y);
				else									gotoxy(x, y);

				printf(CURSOR);
				lastX = x;
				lastY = y;
				break;

			case RIGHT:
				if (CheckMapOver(x + 1, y) == false)	gotoxy(++x, y);
				else									gotoxy(x, y);

				printf(CURSOR);
				lastX = x;
				lastY = y;
				break;

			case LEFT:
				if (CheckMapOver(x - 1, y) == false)	gotoxy(--x, y);
				else									gotoxy(x, y);

				printf(CURSOR);
				lastX = x;
				lastY = y;
				break;
			}
		}
	}
	return make_pair(x, y);
}

bool CheckMapOver(int x, int y)
{
	return x < 0 || y < 0 || x > MAPSIZE - 1 || y > MAPSIZE - 1;
}

void CursorView()
{
	CONSOLE_CURSOR_INFO cursorInfo = { 0, };
	cursorInfo.dwSize = 1;
	cursorInfo.bVisible = FALSE;
	SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursorInfo);
}

string returnMapShape(int x, int y)
{
	if (x == 0)
	{
		if (y == 0)					return "┌";
		else if (y == MAPSIZE - 1)	return "└";
		else						return "├";
	}
	if (x == MAPSIZE - 1)
	{
		if (y == 0)					return "┐";
		else if (y == MAPSIZE - 1)	return "┘";
		else						return "┤";
	}
	if (y == 0)	return "┬";
	if (y == MAPSIZE - 1) return "┴";
	return "┼";
}

void PutStone(int x, int y)
{
	Map[y][x] = (int)!Turn + 1;
}

int Algorithm(int x, int y)
{
	// 1 2 3
	// 8   4
	// 7 6 5
	// y,x 순서
	int directs[8][2] = { {-1, -1}, {-1, 0}, {-1, 1}, {0, 1}, {1, 1}, {1, 0}, {1, -1}, {0, -1} };
	int sum[4] = { 0, };	// 반대편 방향까지 포함해서 세기 때문에 4개만 있으면 됨

	for (int i = 0; i < 8; i++)
	{
		// y증감, x증감 설정
		int yy = directs[i][0];
		int xx = directs[i][1];

		// 한 칸 진행된 상태로 실행
		int Y = y + yy;
		int X = x + xx;

		// X, Y가 맵을 넘어감 == true 거나 내 돌이 아님 == true 면 정지
		while (!(CheckMapOver(X, Y) || Map[Y][X] != (int)!Turn + 1))
		{
			if (i > 3)	sum[i - 4] += 1;
			else		sum[i] += 1;
			Y += yy;
			X += xx;
		}
	}

	for (int i = 0; i < 4; i++)
	{
		if (sum[i] >= 4)	return 1;
	}
	return 0;
}

int Finish()
{
	printf("\n\033[0m");
	switch (Turn)
	{
	case 0:
		printf("백돌");
		break;
	case 1:
		printf("흑돌");
		break;
	}
	printf(" 승. [1]다시하기 [2]게임종료");
	while (1)
	{
		int input = _getch();
		if (input - '0' == 1)		return 1;
		else if (input - '0' == 2)	return 2;
		else						continue;
	}
}