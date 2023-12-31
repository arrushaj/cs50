#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(int argc, string argv[])
{
    string text1 = get_string("Text: ");
    int total_letters = count_letters(text1);
    int total_words = count_words(text1);
    int total_sentences = count_sentences(text1);
    double index = 0.0588 * (double) total_letters / (double) total_words * 100 - 0.296 * (double) total_sentences /
                    (double) total_words * 100 - 15.8;   // index = 0.0588 * L - 0.296 * S - 15.8
    int round_index = round(index);  // Rounds float above and turns into int, chopping off everything after decimal
    if (index < 1)      // Checking index before rounding
    {
        printf("Before Grade 1\n");
    }
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index > 1 && index < 16)
    {
        printf("Grade %i\n", round_index);
    }

}

int count_letters(string text)
{
    int total_letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
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
    return total_letters;
}

int count_words(string text)
{
    int total_words = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 32)
        {
            total_words = total_words + 1;
        }
        else
        {
            total_words = total_words + 0;
        }
    }
    total_words = total_words + 1; // In order to account for word after last space
    return total_words;
}

int count_sentences(string text)
{
    int total_sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text [i] == 33 || text[i] == 46 || text[i] == 63)
        {
            total_sentences = total_sentences + 1;
        }
        else
        {
            total_sentences = total_sentences + 0;
        }
    }
    return total_sentences;
}