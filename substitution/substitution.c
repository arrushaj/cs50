#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

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
        printf("Nice!\n");
        return 0;
        }
    }
}