#include <cs50.h>
#include <stdio.h>

int count_letters(string text)

int main(int argc, string argv[])
{
    string text1 = get_string("Text: ");
    printf("%s\n", text1);
}

int count_letters(string text)
{
    int total_letters = 0;
    for (int i = 0, n = strlen(text); i < n, i++)
    {
        if isupper(text[i])
        {
            total_letters = total_letters + 1;
        }
        if islower(text[i])
        {
            total_letters = total_letters + 1;
        }
        else
        {
            total_letters = total_letters + 0;
        }
    }

}