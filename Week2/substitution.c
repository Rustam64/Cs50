#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string cipher(string substitute, string plaintext);
bool validate(string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if (!validate(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    for (int i = 0; i < 26; i++)
    {
        key[i] = toupper(key[i]);
    }
    string plaintext = get_string("plaintext:");
    char *answer = cipher(key, plaintext);
    printf("ciphertext: %s\n", answer);
    free(answer);
}

bool validate(string key)
{
    for (int i = 0; i < 26; i++)
    {
        key[i] = toupper(key[i]);
    }
    char alphabet[26] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    if (strlen(key) != 26)
    {
        return false;
    }
    for (int i = 0; i < 26; i++)
    {
        char *found = strchr(alphabet, key[i]);
        if (found == NULL)
        {
            printf("Duplicate or invalid letter: %c\n", key[i]);
            return false;
        }
        *found = '*';
    }
    return true;
}

string cipher(string substitute, string plaintext)
{
    int len = strlen(plaintext);
    char *ciphertext = malloc(len + 1);
    for (int i = 0; i < len; i++)
    {
        if (!isalpha(plaintext[i]))
        {
            ciphertext[i] = plaintext[i];
        }
        else if (islower(plaintext[i]))
        {
            ciphertext[i] = tolower(substitute[(plaintext[i]) - 97]);
        }
        else
        {
            ciphertext[i] = substitute[(plaintext[i]) - 65];
        }
    }
    ciphertext[len] = '\0';
    return ciphertext;
}
