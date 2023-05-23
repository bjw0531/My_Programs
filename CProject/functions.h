#pragma once
#include "preprocess.h"

void PriceThread() // 스레드 함수
{
    // 이현웅 담당
}

void gotoxy(int x, int y) // 콘솔 마우스 커서 이동 함수
{
    COORD Pos = { x * 2, y };
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), Pos);
}

void CCprint(struct _CrypCur* CC, int x, int y) // CC 출력 함수
{
    gotoxy(x, y);
    printf("이름 : %s", CC->name);
    gotoxy(x, y + 1);
    printf("가격 : %.2lf", CC->price);
}

void CCinit(struct _CrypCur* CC, const char name[], double price, int idx) // CC 초기화 함수
{
    CC->idx = idx;
    strcpy(CC->name, name);
    CC->price = price;
}
