#include <cs50.h>
#include <stdio.h>

void Gap(int gap);
void Block(int block);
void pyramid(int height, int gap, int block);

int main()
{
    int height = -1;
    while (height <= 0)
    {
        height = get_int("What's the height of the pyramid? ");
    }
    if (height > 0)
    {
        int gap = height - 1;
        int block = 1;
        pyramid(height, gap, block);
    }
}

void Block(int block)
{
    while (block > 0)
    {
        printf("#");
        block--;
    }
}

void Gap(int gap)
{
    for (int i = gap; i > 0; i--)
    {
        printf(" ");
    }
}

void pyramid(int height, int gap, int block)
{
    while (height > 0)
    {
        Gap(gap);
        Block(block);
        printf("  ");
        Block(block);
        printf("\n");
        block++;
        height--;
        gap--;
    }
}
