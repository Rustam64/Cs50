#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

void reading_level(string text);

int main()
{
    string text = get_string("Text: ");
    reading_level(text);
}

void reading_level(string text)
{
    int words = 1, letters = 0, sentences = 0;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (isspace(text[i]))
        {
            words += 1;
        }
        else if (ispunct(text[i]))
        {
            if (text[i] == '!' || text[i] == '.' || text[i] == '?')
            {
                sentences += 1;
            }
        }
        else if (isalpha(text[i]))
        {
            letters += 1;
        }
    }
    float ind = 0.0, L = (100.0 / words * letters), S = (100.0 / words * sentences);
    ind = 0.0588 * L - 0.296 * S - 15.8;
    int index = floor(ind + 0.5);
    if (index > 16.0)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1.0)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
