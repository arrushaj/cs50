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

    for (int i = 0; i < height; i++)  // Row
    {
        // Column
        for (int k = 0; k < height - i - 1; k++)  // How many spaces (Number of rows - 1 - the row indexed from 0)
        {
            printf(" ");
        }
        for (int j = 0; j < i + 1; j++)  // How many hashes (Which row you're in (indexed from 0) + 1)
        {
            printf("#");
        }

        printf("  ");

        // Column
        for (int m = 0; m < i + 1; m++)  // How many hashes (Which row you're in (indexed from 0) + 1)
        {
            printf("#");
        }

         for (int l = 0; l < height - i - 1; l++)  // How many spaces (number of rows - 1 - the row indexed from 0)
        {
            printf(" ");
        }

        printf("\n");
    }
}
