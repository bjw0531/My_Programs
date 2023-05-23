#include "preprocess.h"
#include "functions.h"

int main()
{
    char names[5][50] = { "Soo", "Bang", "Gun", "Soo", "Gang" };
    int prices[5] = { 100,200,300,400,5000000 };

    for (int i = 0; i < 5; i++)
    {
        CCinit(&Crypto[i], names[i], prices[i], i + 1);
    }

    for (int i = 0; i < 5; i++)
    {
        CCprint(&Crypto[i], i * 12, 0);
    }

    gotoxy(0, 5);
    printf("(1) 구매\n(2) 판매");

}	