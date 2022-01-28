#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int unique(string key);

int main(int argc, string argv[])
{
    if (argc != 2)  // If no input
    {
         printf("Missing command-line argument\n");
         return 1;
    }
    if (argc == 2)
    {
        if (strlen(argv[1]) != 26)
        {
        printf("Key must contain 26 characters.\n");
        return 1;
        }
        if (strlen(argv[1]) == 26)
        {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (argv[1][i] == argv[1][j])
                {
                    printf("Each character isn't unique!\n");
                    return 1;
                }
            }
        }
        printf("Nice!\n");
        return 0;
        }
    }
}

int unique(string key);