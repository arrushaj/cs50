#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

int i;
int k;
int j;

    for (int i = 0; i < height; i++)
    {
        for (k = 0; k < height - i - 1; k++)
        {
            printf(" ");
        }
        for (j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
