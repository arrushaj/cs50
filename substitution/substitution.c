#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int uniqueness(string key);

int main(int argc, string argv[])
{
    if (argc != 2)  // If no input
    {
        printf("Usage: ./substitution key\n");
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
            }

            int unique = uniqueness(argv[1]);

            if (unique == 1)
            {
                printf("Each character isn't unique!\n");
                return 1;
            }
            else if (unique == 0)
            {
                printf("Nice!\n");
                string plaintext = get_string("plaintext: ");
                for (int i = 0, m = strlen(plaintext); i < m; i++)
                {
                    int x = 0;                                          // WE WANT TO FIND A WAY TO GET THE CHARACTER OF THE PLAINTEXT STRING AND MAP IT TO THE INDEX OF THE KEY
                    if isupper(plaintext[i])
                    {
                        x = plaintext[i] - 65;
                        plaintext[i] = toupper(argv[1][x]);

                    }
                    if islower(plaintext[i])
                    {
                        x = plaintext[i] - 97;
                        plaintext[i] = tolower(argv[1][x]);
                    }
                }
                string ciphertext = plaintext;
                printf("ciphertext: %s\n", ciphertext);
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