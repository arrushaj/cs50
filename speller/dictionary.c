// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 10;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    node *n = malloc(sizeof(node));
    if (n == NULL)
    {
        return false;
    }
    n = table[index];
    while (n != NULL)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
            free(n);
        }
        else
        {
            n = n->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int index = 0;
    int n = strlen(word);
    for (int i = 0; i < n; i++)
    {
        if (word[i] == '\'')
        {
            index += 0;
        }
        index += (toupper(word[i]) - 'A');
    }
    // TODO: Improve this hash function
    if (index > N - 1)
    {
        index = index % N;
    }
    return index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char buffer[LENGTH + 1];
    while (fscanf(file, "%s", buffer) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, buffer);
        int index = hash(n->word);
        n->next = table[index];
        table[index] = n;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int total = 0;
    node *n = malloc(sizeof(node));
    if (n == NULL)
    {
        return false;
    }
    for (int i = 0; i < N; i++)
    {
        n = table[i];
        while (n != NULL)
        {
            total++;
            n = n->next;
        }
    }
    free(n);
    return total;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cursor = malloc(sizeof(node));
    if (cursor == NULL)
    {
        return false;
    }
    node *tmp = malloc(sizeof(node));
    if (tmp == NULL)
    {
        return false;
    }
    for (int i = 0; i < N; i++)
    {
        tmp = table[i];             // Set 2 pointers equal to linked list
        cursor = table[i];
        while (cursor != NULL)
        {
            cursor = cursor->next;      // Keep moving along the linked list while not orphaning and losing track of where you are
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
