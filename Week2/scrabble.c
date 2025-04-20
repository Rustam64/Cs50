#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void scrabble(string word1, string word2);
int score(string word);

int main()
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");
    scrabble(word1, word2);
}

void scrabble(string word1, string word2)
{
    if (score(word1) > score(word2))
    {
        printf("Player 1 wins!\n");
    }
    else if (score(word1) < score(word2))
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
int score(string word)
{
    int score = 0;
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        char letter = tolower(word[i]);
        if (letter == 'a' || letter == 'e' || letter == 'i' || letter == 'l' || letter == 'n' ||
            letter == 'o' || letter == 'r' || letter == 's' || letter == 't' || letter == 'u')
        {
            score += 1;
        }
        else if (letter == 'd' || letter == 'g')
        {
            score += 2;
        }
        else if (letter == 'b' || letter == 'c' || letter == 'm' || letter == 'p')
        {
            score += 3;
        }
        else if (letter == 'f' || letter == 'h' || letter == 'v' || letter == 'w' || letter == 'y')
        {
            score += 4;
        }
        else if (letter == 'k')
        {
            score += 5;
        }
        else if (letter == 'j' || letter == 'x')
        {
            score += 8;
        }
        else if (letter == 'z' || letter == 'q')
        {
            score += 10;
        }
        else
        {
            printf("invalid input!\n");
        }
    }
    return score;
}
