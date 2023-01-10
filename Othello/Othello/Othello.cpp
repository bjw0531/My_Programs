#include <iostream>
#include <algorithm>
#include <conio.h>
#include <Windows.h>
#include <vector>
using namespace std;

#define mapsize 8

// . = -1
// O = 0
// X = 1

bool turn;
char Exchange(int i);
int Count(int arr[mapsize][mapsize], int i);
void CursorView();
int DoLogic(int Y, int X, int v, int arr[][mapsize]);


class map
{
public:
    int arr[mapsize][mapsize];

    // -1로 초기화
    void initialize()
    {
        memset(arr, -1, sizeof(arr));
    }

    // 배열 y,x값을 v로 바꿉니다 이미 값이 있으면 -1을 반환합니다
    int push(int y, int x, int v)
    {
        if (arr[y - 1][x - 1] == -1)  arr[y - 1][x - 1] = v;
        else return -1;
    }


}mp;

class display
{
public:
    // map의 2차원 배열을 받아서 출력합니다.
    void draw(int arr[mapsize][mapsize], int mode)
    {
        printf(" --  --  --  --  --  --  --  --  --  --\n");
        printf("| .   1   2   3   4   5   6   7   8    | 현재 플레이어 : %c\n", Exchange(turn));
        for (int i = 0; i < mapsize; i++)
        {
            printf("\n| %c   ", i + 'a');
            for (int j = 0; j < mapsize; j++)
            {
                printf("%c   ", Exchange(arr[i][j]));
            }
            printf(" |\n");
        }
        printf(" --  --  --  --  --  --  --  --  --  --\n");
        printf("컴퓨터 (O) : %d점 vs 사용자 (X) : %d점\n", Count(arr, 0), Count(arr, 1));

        // 승리 시에 출력
        if (mode == 1)
        {
            if (Count(arr, 0) == Count(arr, 1)) printf("무승부.");
            else
            {
                bool check = Count(arr, 0) < Count(arr, 1);
                printf("%c 승리.", Exchange(check));
            }
            printf(" [1]다시하기 [2]나가기");
        }
    }

    // 화면을 지웁니다.
    void clear()
    {
        system("cls");
    }
}dp;



int main()
{
initial:
    // 초기화
    turn = false;
    mp.initialize();
    mp.push(4, 4, 0);
    mp.push(5, 5, 0);
    mp.push(4, 5, 1);
    mp.push(5, 4, 1);
    CursorView();

    int x, y;
    while (1)
    {
        if (Count(mp.arr, -1) == 0)  goto Win;
        if (Count(mp.arr, 0) == 0)   goto Win;
        if (Count(mp.arr, 1) == 0)   goto Win;
        dp.clear();
        dp.draw(mp.arr, 0);


        // 잘못된 값이면 다시 받기
        x = _getch() - '0'; // '0' = 30
        if (x < 0 || x > 10) continue;

        y = _getch() - 'a' + 1; // 'a' = 61
        if (y < 0 || y > 9) continue;


        if (mp.push(y, x, turn) == -1)        continue;
        if (DoLogic(y, x, turn, mp.arr) == -1) continue;

        turn = !turn;
    }

Win:
    dp.clear();
    dp.draw(mp.arr, 1);
    int tmp = _getch() - '0';
    if (tmp == 1)  goto initial;
    else           return 0;

}



// 정수값인 요소를 문자로 바꿔 return
char Exchange(int i)
{
    if (i == -1)  return '.';
    if (i == 0)   return 'O';
    if (i == 1)   return 'X';
}

// 2차원 배열에서 i의 갯수를 구하는 함수
int Count(int arr[mapsize][mapsize], int i)
{
    return count(&arr[0][0], &arr[0][0] + mapsize * mapsize, i);
}

// 커서 숨기기
void CursorView()
{
    CONSOLE_CURSOR_INFO cursorInfo = { 0, };
    cursorInfo.dwSize = 1; //커서 굵기 (1 ~ 100)
    cursorInfo.bVisible = FALSE; //커서 Visible TRUE(보임) FALSE(숨김)
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursorInfo);
}

// 가로, 세로, 대각선에 있는 상대방의 돌을 바꿉니다
int DoLogic(int Y, int X, int v, int arr[][mapsize])
{
    // 0 1 2
    // 7 * 3
    // 6 5 4  -> 이 순서대로 8방을 확인, 상대방의 돌이 아닌 자신의 돌이 나오면 바꾸기 종료 {y, x}
    int directs[8][2] = { {-1, -1}, {-1, 0},{-1, 1},{0, 1},{1, 1},{1, 0},{1, -1},{0, -1} };
    int x, y, xx, yy;
    int opposite = int(!v);
    bool CheckMapOver;
    bool CheckSomethingTodo = false;
    for (int i = 0; i < 8; i++)
    {
        xx = directs[i][1]; // x 증감
        yy = directs[i][0]; // y 증감
        x = X + xx - 1; // x 위치 (-1은 index값에 +1 한 값이 인수로 들어오기 때문)
        y = Y + yy - 1; // y 위치
        CheckMapOver = x < 0 || y < 0 || x > 7 || y > 7; // 가르키는 부분이 맵을 넘어갔으면 true
        vector<pair<int, int>> vec(8, { -1,-1 });

        // n번째 방향이 상대 돌이 아니거나 맵을 넘어갔다면
        if (CheckMapOver || arr[y][x] != opposite)  continue;

        for (int j = 0; !CheckMapOver && arr[y][x] == opposite; j++)
        {
            vec[j].first = y;
            vec[j].second = x;
            x += xx;
            y += yy;
            CheckMapOver = x < 0 || y < 0 || x > 7 || y > 7;
        } // 끝났다면 MapOver 되었거나 다음 돌이 상대방의 돌이 아닌 것

        if (CheckMapOver)  continue;
        else if (arr[y][x] == v)
        {
            CheckSomethingTodo = true;
            for (auto i : vec)
            {
                arr[i.first][i.second] = v;
            }
        }
    }

    // 아무것도 하지 않았다면 -1 반환
    if (CheckSomethingTodo)  return 0;
    else
    {
        arr[Y - 1][X - 1] = -1;
        return -1;
    }
}