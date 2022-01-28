#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int uniqueness(string key);

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
            for (int i = 0, a = strlen(argv[1]); i < a; i++)
            {
                if (isalpha(argv[1][i]) == 0)
                {
                    printf("Not alphabetical character.\n");
                    return 1;
                }
            //    if (argv[1][i] > 90 && argv[1][i] < 97)
            //    {
            //        printf("Not alphabetical character.\n");
            //        return 1;
            //    }
            //    if (argv[1][i] < 65)
            //    {
            //        printf("Not alphabetical character.\n");
            //        return 1;
            //    }
            //    if (argv[1][i] > 123)
            //    {
            //        printf("Not alphabetical character.\n");
            //        return 1;
            }

            int unique = uniqueness(argv[1]);

            if (unique == 1)
            {
                printf("Each character isn't unique!\n");
                return 1;
            }
            else if (unique == 0)
            {
                for (int j = 0, n = strlen(arg[1][j]); j < n; j++)
                {
                    
                }
                printf("Nice!\n");
                string plaintext = get_string("plaintext: ");
                for (int i = 0, n = strlen(plaintext); i < n; i++)
                {

                }
                return 0;
            }
        }
    }
}

int uniqueness(string key)
{
    int unique = 0;
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (key[i] == key[j])
            {
                unique = 1;
            }
        }
    }
    return unique;
}