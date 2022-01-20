#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || n > height);

    for (int i = 0; i < height; i++)
    {
        for (int k = 0; )
        for (int j = 0; j < height; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
