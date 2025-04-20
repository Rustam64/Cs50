// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];
int dictionary_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    char lowercase_word[LENGTH + 1];
    int i = 0;
    while (word[i] != '\0' && i < LENGTH)
    {
        lowercase_word[i] = tolower(word[i]);
        i++;
    }
    lowercase_word[i] = '\0';
    unsigned int index = hash(lowercase_word);
    node *temp = table[index];
    while (temp != NULL)
    {
        if (strcmp(temp->word, lowercase_word) == 0)
        {
            return true;
        }
        temp = temp->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int temp = 0;
    if ((toupper(word[1]) - 'A') > 14)
    {
        temp = 1;
    }
    return ((toupper(word[0]) - 'A') * 2) + temp;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word_holder[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    while (fscanf(file, "%45s", word_holder) == 1)
    {
        unsigned int index = hash(word_holder);
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }
        strcpy(new_node->word, word_holder);
        dictionary_size++;
        new_node->next = table[index];
        table[index] = new_node;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            node *temp = ptr;
            ptr = ptr->next;
            free(temp);
        }
        table[i] = NULL;
    }
    return true;
}
