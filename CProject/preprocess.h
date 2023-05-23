#pragma once
#include <stdio.h>
#include <windows.h>
#include <string.h>
#include <process.h>
#include <stdlib.h>
typedef long long ll;

struct _CrypCur // 가상화폐 구조체
{
    char name[50];
    double price;
    int idx;
} Crypto[5];