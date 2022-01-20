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

    for (int i = 0; i < height; i++)  //row
    {
        for (int k = 0; k < height - i - 1; k++)  //how many spaces (number of rows - 1 - the row starting from 0)
        {
            printf(" ");
        }
        for (int j = 0; j < i + 1; j++)  //how many hashes (which row you're in (starting from 0) + 1)
        {
            printf("#");
        }

        printf("  \n");

        for (int )
        printf("\n");
    }
}
